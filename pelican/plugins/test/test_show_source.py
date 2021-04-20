import pathlib

import pytest

import pelican


def _site(output_path, conf_filename):
    datadir = pathlib.Path(__file__).parent / "data"
    args = [
        datadir / "content",
        "-o",
        output_path,
        "-s",
        datadir / conf_filename,
        "--relative-urls",
        "--debug"
    ]
    pelican.main([str(a) for a in args])


@pytest.fixture(scope="module")
def site_autoext_true(tmp_path_factory):
    output = tmp_path_factory.getbasetemp()
    _site(output, "pelicanconf_autoext_true.py")
    yield output


@pytest.fixture(scope="module")
def site_autoext_false(tmp_path_factory):
    output = tmp_path_factory.getbasetemp()
    _site(output, "pelicanconf_autoext_false.py")
    yield output

@pytest.fixture(scope="module")
def site_autoext_default(tmp_path_factory):
    output = tmp_path_factory.getbasetemp()
    _site(output, "pelicanconf.py")
    yield output

def _test_show_source(site, src_extension):
    tag = "esse-quam-laboriosam-at-accusantium"

    # verify the original source has been transferred
    assert (site / (tag + src_extension)).exists()
    # and rendered
    assert (site / (tag + ".html")).exists()

    # verify presence of "Show source" reference
    subtxt = f'<a href="./{tag}{src_extension}">Show source</a>'
    assert subtxt in (site / (tag + ".html")).read_text()


def test_show_source_autoext_default(site_autoext_default):
    _test_show_source(site_autoext_default, ".txt")


def test_show_source_autoext_false(site_autoext_false):
    _test_show_source(site_autoext_false, ".txt")


def test_show_source_autoext_true(site_autoext_true):
    _test_show_source(site_autoext_true, ".md")
