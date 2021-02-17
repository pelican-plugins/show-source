import pathlib

import pytest

import pelican


@pytest.fixture(scope="module", autouse=True)
def site(tmp_path_factory):
    output = tmp_path_factory.getbasetemp()
    datadir = pathlib.Path(__file__).parent / "data"
    args = [
        datadir / "content",
        "-o",
        output,
        "-s",
        datadir / "pelicanconf.py",
        "-D",
        "--relative-urls",
    ]
    pelican.main([str(a) for a in args])
    yield output


def test_show_source(site):
    tag = "esse-quam-laboriosam-at-accusantium"
    assert (site / (tag + ".html")).exists()
    assert (tag + ".txt") in (site / (tag + ".html")).read_text()
