from pathlib import Path

from rbase24.config import Base24ViewerConfig


def test_config_default_scheme_dir():
    sd = Base24ViewerConfig.default_scheme_dir()
    assert sd == Path("~/.local/share/tinted-themeing/schemes").expanduser()


def test_config_default_config_path():
    cp = Base24ViewerConfig.default_config_path()
    assert cp == Path("~/.config/rbase24/config.ini").expanduser()


def test_config_default_config():
    dc = Base24ViewerConfig.default_config()
    assert dc == {"scheme_dir": Base24ViewerConfig.default_scheme_dir()}


def test_config_local():
    cf = Path(__file__).parent / "config.ini"
    cfg = Base24ViewerConfig(cf)
    assert cfg.scheme_dir.name == "schemes"


def test_config_bad_path():
    badcfg = Path("notthere")
    cfg = Base24ViewerConfig(badcfg)
    assert cfg.scheme_dir == Path("~/.local/share/tinted-themeing/schemes").expanduser()
