import rbase24


def test_base_scheme_dir():
    rbase24.scheme_dir()


def test_base_load_file():
    scheme = rbase24.load_scheme("nord")
    assert scheme["base00"] == ""
