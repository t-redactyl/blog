#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

# This file is only used if you use `make publish` or
# explicitly specify it as your config file.

import os
import sys
sys.path.append(os.curdir)
from pelicanconf import *

SITEURL = 'http://t-redactyl.github.io'
RELATIVE_URLS = False

FEED_ALL_ATOM = 'feeds/all.atom.xml'
CATEGORY_FEED_ATOM = 'feeds/%s.atom.xml'

DELETE_OUTPUT_DIRECTORY = False

# Following items are often useful when publishing

#DISQUS_SITENAME = ""
# Change this for your google analytics account
GOOGLE_ANALYTICS = "UA-66946155-1"

GITHUB_REPO = 'git@github.com:t-redactyl/t-redactyl.github.io.git'
SUBMODULE_NAME = 'output'

