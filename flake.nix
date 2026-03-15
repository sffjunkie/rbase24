{
  description = "CLI Base16 ciolor scheme viewer";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";

    git-hooks = {
      url = "github:cachix/git-hooks.nix";
      inputs.nixpkgs.follows = "nixpkgs";
    };

    pyproject-nix = {
      url = "github:pyproject-nix/pyproject.nix";
      inputs.nixpkgs.follows = "nixpkgs";
    };

    pyproject-build-systems = {
      url = "github:pyproject-nix/build-system-pkgs";
      inputs.pyproject-nix.follows = "pyproject-nix";
      inputs.uv2nix.follows = "uv2nix";
      inputs.nixpkgs.follows = "nixpkgs";
    };

    uv2nix = {
      url = "github:pyproject-nix/uv2nix";
      inputs.pyproject-nix.follows = "pyproject-nix";
      inputs.nixpkgs.follows = "nixpkgs";
    };
  };

  outputs =
    {
      self,
      git-hooks,
      nixpkgs,
      pyproject-build-systems,
      pyproject-nix,
      uv2nix,
      ...
    }:
    let
      inherit (nixpkgs) lib;

      forAllSystems = lib.genAttrs [
        "x86_64-linux"
      ];

      pyproject = pyproject-nix.lib.project.loadPyproject {
        projectRoot = ./.;
      };
      project_name = pyproject.pyproject.project.name;

      workspace = uv2nix.lib.workspace.loadWorkspace {
        workspaceRoot = ./.;
      };

      overlay = workspace.mkPyprojectOverlay {
        sourcePreference = "wheel";
      };

      pythonSets = forAllSystems (
        system:
        let
          pkgs = nixpkgs.legacyPackages.${system};
          python = pkgs.python3;
        in
        (pkgs.callPackage pyproject-nix.build.packages {
          inherit python;
        }).overrideScope
          (
            lib.composeManyExtensions [
              pyproject-build-systems.overlays.wheel
              overlay
            ]
          )
      );
    in
    {
      packages = forAllSystems (system: {
        default = pythonSets.${system}.mkVirtualEnv "${project_name}-env" workspace.deps.default;
      });

      apps = forAllSystems (system: {
        default = {
          type = "app";
          program = "${self.packages.${system}.default}/bin/${project_name}";
          meta = {
            description = "CLI Base16 ciolor scheme viewer";
            homepage = "https://github.com/sffjunkie/${project_name}";
            license = lib.licenses.asl20;
          };
        };
      });

      checks = forAllSystems (
        system:
        let
          pkgs = nixpkgs.legacyPackages.${system};
          editableOverlay = workspace.mkEditablePyprojectOverlay { root = "$REPO_ROOT"; };
          pythonSet = pythonSets.${system}.overrideScope editableOverlay;
          virtualenv = pythonSet.mkVirtualEnv "${project_name}-env" workspace.deps.all;
        in
        {
          pre-commit-check = git-hooks.lib.${system}.run {
            src = ./.;
            hooks = {
              end-of-file-fixer.enable = true;
              ruff = {
                enable = true;
                package = pkgs.ruff;
              };
              trim-trailing-whitespace.enable = true;

              ty = {
                enable = true;
                name = "ty Python type checker";
                entry = "bash -c '${pkgs.ty}/bin/ty check --python=${virtualenv}/bin/python3'";
              };
            };
          };
        }
      );

      devShells = forAllSystems (
        system:
        let
          pkgs = nixpkgs.legacyPackages.${system};
          editableOverlay = workspace.mkEditablePyprojectOverlay { root = "$REPO_ROOT"; };
          pythonSet = pythonSets.${system}.overrideScope editableOverlay;
          virtualenv = pythonSet.mkVirtualEnv "${pyproject.pyproject.project.name}-env" workspace.deps.all;
        in
        {

          default = pkgs.mkShell {
            packages = [
              virtualenv
              pkgs.just
              pkgs.python3Packages.ty
              pkgs.uv
            ];
            env = {
              NIX_DEVSHELL_PROJECT = project_name;
              UV_PYTHON_DOWNLOADS = "never";
              UV_PYTHON = "${virtualenv}/bin/python3";
            };
            shellHook = ''
              unset PYTHONPATH
              export REPO_ROOT=$(git rev-parse --show-toplevel)
            '';
          };
        }
      );
    };
}
