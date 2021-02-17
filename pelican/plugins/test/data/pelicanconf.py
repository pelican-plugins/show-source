import pathlib

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
SHOW_SOURCE_IN_SECTION = True
SHOW_SOURCE_ON_SIDEBAR = True
SHOW_SOURCE_ALL_POSTS = True
THEME_TEMPLATES_OVERRIDES = [
    thisdir / "templates",
]
THEME_TEMPLATES_OVERRIDES = [
    thisdir / "templates",
]
