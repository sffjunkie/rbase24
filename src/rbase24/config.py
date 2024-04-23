import os
from pathlib import Path
from configparser import ConfigParser


class Base24ViewerConfig:
    def __init__(self, config_file: Path | None = None):
        self.scheme_dir = self._scheme_dir(config_file)

    def _scheme_dir(self, config_file: Path | None = None) -> Path:
        scheme_dir = os.environ.get("BASE24_SCHEME_DIR", None)
        if scheme_dir is not None:
            return Path(scheme_dir)

        default_dir = Path("~/.local/share/base24/schemes").expanduser()
        cf = self._read_config(config_file)
        if cf is None:
            return default_dir

        scheme_dir = cf.get("rbase24", "scheme_dir")
        if scheme_dir is not None:
            return Path(scheme_dir)

        return default_dir

    def _read_config(self, config_file: Path | None = None):
        try:
            if config_file is None:
                cf = self._config_path()
            else:
                cf = config_file
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
