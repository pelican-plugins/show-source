import collections
import itertools
import pathlib
import enum

import pytest
import pelican

# makes easier to handle flags
class Flags(enum.IntEnum):
    SHOW_SOURCE_AUTOEXT = 0
    SHOW_SOURCE_ALL_POSTS = 1
    SHOW_SOURCE_ON_SIDEBAR = 2
    SHOW_SOURCE_IN_SECTION = 3
Pconf = collections.namedtuple("Pconf", [f.name for f in Flags])


@pytest.fixture(scope="module")
def site(request, tmp_path_factory):
    from pelican import settings

    # this will pass the test configuration down to the pelicanconf.py
    settings.DEFAULT_CONFIG["PCONF"] = Pconf(*request.param)

    # renders a simple site with three pages
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

    # write a file with a name like (for troubleshooting):
    #  AUTOEXT=0-ALL_POSTS=1-ON_SIDEBAR=0-IN_SECTION=1
    (output / "-".join(f"{k[12:]}={int(v)}" for k, v in zip(Pconf._fields, request.param))).touch()
    yield output


FLAGS = [
    (p, False, True, False,)
    for p, in sorted(itertools.product([True, False], repeat=1))
]
@pytest.mark.parametrize("site", FLAGS, indirect=["site"])
def test_autoext(site):
    "test the SHOW_SOURCE_AUTOEXT writes the correct file extension"
    from pelican import settings
    pconf = settings.DEFAULT_CONFIG["PCONF"]

    tag = "esse-quam-laboriosam-at-accusantium"

    # verify extension flags
    src_extension = ".md" if pconf.SHOW_SOURCE_AUTOEXT else ".txt"

    # verify the page has been rendered
    assert (site / (tag + ".html")).exists()
    # verify the original source has been transferred
    assert (site / (tag + src_extension)).exists()


FLAGS = [
    (p, q, r, s)
    for p, q, r, s in sorted(itertools.product([True, False], repeat=4))
]
@pytest.mark.parametrize("site", FLAGS, indirect=["site"])
def test_site(site):
    "test all the possible flags use"
    from pelican import settings
    pconf = settings.DEFAULT_CONFIG["PCONF"]

    tag = "esse-quam-laboriosam-at-accusantium"
    src_extension = ".md" if pconf.SHOW_SOURCE_AUTOEXT else ".txt"

    # files have the inline show source?
    has_insection = []
    for e in [ "", "-2", "-3"]:
        subtxt = f"<a href=\"./{tag}{e}{src_extension}\">Show source</a>"
        has_insection.append(subtxt in (site / (tag + f"{e}.html")).read_text())

    # files have the in sidebar show source?
    has_sidebar = []
    for e in [ "", "-2", "-3"]:
        subtxt = f"(<a href=\"./{tag}{e}{src_extension}\">.. show source</a>)"
        has_sidebar.append(subtxt in (site / (tag + f"{e}.html")).read_text())


    if not (pconf.SHOW_SOURCE_IN_SECTION or pconf.SHOW_SOURCE_ON_SIDEBAR):
        assert not any(has_insection)
        assert not any(has_sidebar)

    if not pconf.SHOW_SOURCE_IN_SECTION:
        assert not any(has_insection)

    if not pconf.SHOW_SOURCE_ON_SIDEBAR:
        assert not any(has_sidebar)

    if pconf.SHOW_SOURCE_ALL_POSTS:
        if pconf.SHOW_SOURCE_IN_SECTION:
            assert all(has_insection)
        if pconf.SHOW_SOURCE_ON_SIDEBAR:
            assert all(has_sidebar)
    else:
        if pconf.SHOW_SOURCE_IN_SECTION:
            assert has_insection == [True, False, True]
        if pconf.SHOW_SOURCE_ON_SIDEBAR:
            assert has_sidebar == [True, False, True]

