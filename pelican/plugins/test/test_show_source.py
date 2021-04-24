import itertools

import pathlib

import pytest
import pelican


@pytest.fixture(scope="module")
def site(request, tmp_path_factory):
    from pelican import settings
    from collections import namedtuple

    Pconf = namedtuple("Pconf", [ k for k, _ in request.param])
    settings.DEFAULT_CONFIG["PCONF"] = Pconf(*[ v for _, v in request.param])

    output = tmp_path_factory.mktemp("site")
    datadir = pathlib.Path(__file__).parent / "data"
    args = [
        datadir / "content",
        "-o",
        output,
        "-s",
        datadir / "pelicanconf.py",
        "--relative-urls",
        "--debug"
    ]
    pelican.main([str(a) for a in args])
    # write a file
    (output / "-".join(str(v) for _, v in request.param)).touch()
    yield output


FLAGS = [
    (
        (f"SHOW_SOURCE_AUTOEXT", p,),
        (f"SHOW_SOURCE_ON_SIDEBAR", q),
        (f"SHOW_SOURCE_IN_SECTION", r),
        (f"SHOW_SOURCE_ALL_POSTS", s),
    )
    for p, q, r, s in sorted(itertools.product([True, False], repeat=4))
]

@pytest.mark.parametrize("site", FLAGS, indirect=["site"])
def test_site(site):
    from pelican import settings

    pconf = settings.DEFAULT_CONFIG["PCONF"]
    tag = "esse-quam-laboriosam-at-accusantium"


    # verify extension flags
    src_extension = ".md" if pconf.SHOW_SOURCE_AUTOEXT else ".txt"

    # verify the original source has been transferred
    assert (site / (tag + src_extension)).exists()
    # and rendered
    assert (site / (tag + ".html")).exists()


    # verify presence of "Show source" links
    if pconf.SHOW_SOURCE_ALL_POSTS or pconf.SHOW_SOURCE_ON_SIDEBAR:
        subtxt = f'<a href="./{tag}{src_extension}">Show source</a>'
        assert subtxt in (site / (tag + ".html")).read_text()

