from pathlib import Path

from rbase24.scheme import load_scheme, list_schemes
from rbase24.config import Base24ViewerConfig


def test_scheme_load_base16_scheme():
    cf = Path(__file__).parent / "config.ini"
    cfg = Base24ViewerConfig(cf)
    scheme_dir = cfg.scheme_dir
    scheme_dir = Path(__file__).parent / scheme_dir
    scheme = load_scheme(scheme_dir / "base16" / "horizon-light.yaml")
    assert "fdf0ed" == scheme["palette"]["base00"]


def test_scheme_load_base24_scheme():
    cf = Path(__file__).parent / "config.ini"
    cfg = Base24ViewerConfig(cf)
    scheme_dir = cfg.scheme_dir
    scheme_dir = Path(__file__).parent / scheme_dir
    scheme = load_scheme(scheme_dir / "base24" / "brogrammer.yaml")
    assert "524fb9" == scheme["palette"]["base17"]


def test_scheme_list_schemes():
    cf = Path(__file__).parent / "config.ini"
    cfg = Base24ViewerConfig(cf)
    scheme_dir = cfg.scheme_dir
    scheme_dir = Path(__file__).parent / scheme_dir

    assert 9 == len(list_schemes(scheme_dir))
