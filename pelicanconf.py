#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals
import os

AUTHOR = u'Jodie Burchell'
SITENAME = u'Standard error'

SITEURL = ''

PATH = 'content'

TIMEZONE = 'Australia/Melbourne'

DEFAULT_LANG = u'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

DEFAULT_PAGINATION = 5

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True

# These are my nice configurations
THEME = os.path.join(os.path.dirname(os.path.realpath(__file__)), "theme")
USE_MATHJAX = True
ARCHIVES_URL = 'archives.html'
TYPOGRIFY = True
ARTICLE_URL = 'blog/{date:%Y}/{date:%m}/{slug}.html'
ARTICLE_SAVE_AS = 'blog/{date:%Y}/{date:%m}/{slug}.html'

AUTHOR_GITHUB = 't-redactyl'
AUTHOR_TWITTER = 't_redactyl'

STATIC_PATHS = ['images', 'extra/robots.txt', 'extra/favicon.png', 'figure']
EXTRA_PATH_METADATA = {
    'extra/robots.txt': {'path': 'robots.txt'},
    'extra/favicon.png': {'path': 'favicon.png'}
}
SITESUBTITLE = u'from scientist to data scientist'
SITE_DESCRIPTION = u"My name is Jodie Burchell and I'm a data scientist living in the beautiful city of Melbourne, Australia. This blog is a collection of my data science projects and things I've learned using R, Python, Stata and other tools. The opinions expressed here are my own and do not reflect on my employer."

# Google embed plugin
PLUGINS = ['google_embed']
