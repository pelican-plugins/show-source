import pathlib
from pelican import settings

thisdir = pathlib.Path(__file__).parent

AUTHOR = "Mrs. Joanne Cunningham"
SITENAME = "Nostrum eaque delectus ..."
SITEURL = ""

PATH = "content"
ARTICLE_PATHS = [
    "articles",
]

TIMEZONE = "America/New_York"

DEFAULT_LANG = "en"

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = False
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = (
    ("Pelican", "https://getpelican.com/"),
    ("Python.org", "https://python.org/"),
)

DEFAULT_PAGINATION = 10

STATIC_PATHS = []

PLUGINS = [
    "show_source",
]
THEME_TEMPLATES_OVERRIDES = [
    thisdir / "templates",
]
THEME_TEMPLATES_OVERRIDES = [
    thisdir / "templates",
]

pconf = settings.DEFAULT_CONFIG["PCONF"] # set in the test_show_source.py
SHOW_SOURCE_AUTOEXT = pconf.SHOW_SOURCE_AUTOEXT
SHOW_SOURCE_ON_SIDEBAR = pconf.SHOW_SOURCE_ON_SIDEBAR
SHOW_SOURCE_IN_SECTION = pconf.SHOW_SOURCE_IN_SECTION
SHOW_SOURCE_ALL_POSTS = pconf.SHOW_SOURCE_ALL_POSTS
