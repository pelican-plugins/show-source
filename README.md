Show Source: A Plugin for Pelican
=================================

[![Build Status](https://img.shields.io/github/workflow/status/pelican-plugins/show-source/build)](https://github.com/pelican-plugins/show-source/actions)
[![PyPI Version](https://img.shields.io/pypi/v/pelican-show-source)](https://pypi.org/project/pelican-show-source/)
![License](https://img.shields.io/pypi/l/pelican-show-source?color=blue)

This Pelican plugin allows you to place a link to your posts’ source content files in the same way that [Sphinx][] does. It works for both pages and articles.

Installation
------------

This plugin can be installed via:

    python -m pip install pelican-show-source

For more detailed plugin installation instructions, please refer to the [Pelican Plugin Documentation][].

Configuration
-------------

To enable the plugin, ensure that you have `SHOW_SOURCE_ON_SIDEBAR = True` or `SHOW_SOURCE_IN_SECTION = True` in your settings file.

Making Source Available for Posts
---------------------------------

In order to mark posts so that their source may be seen, use the following metadata fields (unless overridden) for reStructuredText documents:

```rst
:show_source: True
```

Alternatively, for Markdown syntax:

```markdown
Show_source: True
```

The plugin will render your source document URL to a corresponding `article.show_source_url` (or `page.show_source_url`) attribute, which is then accessible in the site templates.

Show Source in the Templates
----------------------------

To get the “show source“ links to display in the article or page you will have to modify your theme, either as a sidebar display or at the foot of an article.

### Article or Page Sidebar Display

How to get the source link to appear in the sidebar using the [pelican-bootstrap3][] theme:

```html
{% if SHOW_SOURCE_ON_SIDEBAR %}
    {% if (article and article.show_source_url) or (page and page.show_source_url) %}
        <li class="list-group-item"><h4><i class="fa fa-tags fa-file-text"></i><span class="icon-label">This Page</span></h4>
            <ul class="list-group">
                <li class="list-group-item">
                    {% if article %}
                    <a href="{{ SITEURL }}/{{ article.show_source_url }}">Show source</a>
                    {% elif page %}
                    <a href="{{ SITEURL }}/{{ page.show_source_url }}">Show source</a>
                    {% endif %}
                </li>
            </ul>
        </li>
    {% endif %}
{% endif %}
```

### Article Footer Display

Following is some code (yes, [pelican-bootstrap3][] again) to enable a source link at the bottom of an article:

```html
{% if SHOW_SOURCE_IN_SECTION %}
    {% if article and article.show_source_url %}
    <section class="well" id="show-source">
        <h4>This Page</h4>
        <ul>
            <a href="{{ SITEURL }}/{{ article.show_source_url }}">Show source</a>
        </ul>
    </section>
    {% endif %}
{% endif %}
```

Overriding Default Plugin Behaviour
-----------------------------------

The default behaviour of the plugin is that revealing source is enabled on a case-by-case basis. This can be changed by the use of `SHOW_SOURCE_ALL_POSTS = True` in the settings file. This does mean that the plugin will publish all source documents no matter whether `show_source` is set in the metadata or not.

Unless overridden, each document is saved as the article or page slug attribute with a `.txt` extension.

So for example, if your configuration had `ARTICLE_SAVE_AS` configured like so:

```python
ARTICLE_SAVE_AS = "posts/{date:%Y}/{date:%m}/{slug}/index.html"
```

… your static HTML post and source text document will be like the following:

```text
posts/2016/10/welcome-to-my article/index.html
posts/2016/10/welcome-to-my article/welcome-to-my article.txt
```

You can add the `SHOW_SOURCE_FILENAME` variable in your settings file to override the source file name, so you could set the following:

```python
SHOW_SOURCE_FILENAME = "my_source_file.txt"
```

So with the `ARTICLE_SAVE_AS` configured as above, the files would be saved
thus:

```text
posts/2016/10/welcome-to-my article/index.html
posts/2016/10/welcome-to-my article/my_source_file.txt
```

This is the same behaviour for pages as well.

Contributing
------------

Contributions are welcome and much appreciated. Every little bit helps. You can contribute by improving the documentation, adding missing features, and fixing bugs. You can also help out by reviewing and commenting on [existing issues][].

To start contributing to this plugin, review the [Contributing to Pelican][] documentation, beginning with the **Contributing Code** section.

[existing issues]: https://github.com/pelican-plugins/show-source/issues
[Contributing to Pelican]: https://docs.getpelican.com/en/latest/contribute.html

License
-------

This project is licensed under the AGPL-3.0 license.


[Pelican Plugin Documentation]: https://docs.getpelican.com/en/latest/plugins.html
[Sphinx]: https://www.sphinx-doc.org/
[pelican-bootstrap3]: https://github.com/getpelican/pelican-themes/tree/master/pelican-bootstrap3
