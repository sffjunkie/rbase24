import os
from pathlib import Path
from configparser import ConfigParser

import yaml
import slugify
from .typedefs import ColorScheme, SchemeDB


class Base24ViewerConfig:
    def __init__(self):
        self.scheme_dir = self._scheme_dir()

    def _scheme_dir(self) -> Path:
        scheme_dir = os.environ.get("BASE24_SCHEME_DIR", None)
        if scheme_dir is not None:
            return Path(scheme_dir)

        default_dir = Path("~/.local/share/base24/schemes").expanduser()
        cf = self._read_config()
        if cf is None:
            return default_dir

        scheme_dir = cf.get("rbase24", "scheme_dir")
        if scheme_dir is not None:
            return Path(scheme_dir)

        return default_dir

    def _read_config(self):
        try:
            cf = self._config_path()
            cp = ConfigParser()
            cp.read(cf)
            return cp
        except IOError:
            return None

    def _config_path(self) -> Path:
        xdg_config = os.environ.get("XDG_CONFIG_HOME", "~/.config")
        xdg_config_dir = Path(xdg_config).expanduser()

        config_dir = xdg_config_dir / "rbase24"
        config_file = config_dir / "config.ini"
        if not config_file.exists():
            raise IOError(f"Unable to find config.ini in {config_dir}")
        return config_file


def load_scheme(scheme_file: Path) -> ColorScheme:
    with open(scheme_file, "r") as fp:
        data = yaml.load(fp.read(-1), yaml.SafeLoader)

        palette = data.get("palette", None)
        if palette is None:
            raise ValueError(
                f"Scheme file {scheme_file} must contain a 'palette' entry"
            )

        system = data.get("system", None)
        if system is None:
            if len(palette) == 16:
                system = "base16"
            else:
                system = "base24"

        slug = data.get("slug")
        if slug is None:
            slug = slugify.slugify(scheme_file.stem, only_ascii=True)

        description = data.get("description", "")
        variant = data.get("variant", "unknown")

        return ColorScheme(
            name=data["name"],
            author=data["author"],
            system=system,
            slug=slug,
            description=description,
            variant=variant,
            palette=palette,
        )


def load_schemes(file_spec: str = "*") -> SchemeDB:
    config = Base24ViewerConfig()

    if "*" not in file_spec:
        fs = file_spec + "*"
    else:
        fs = file_spec

    if not fs.endswith(".yaml"):
        fs = fs + ".yaml"

    schemes = {}
    files = config.scheme_dir.glob(fs)
    for scheme_file in files:
        schemes[scheme_file.name] = load_scheme(scheme_file)

    return schemes
