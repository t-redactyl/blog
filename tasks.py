# -*- coding: utf-8 -*-

import os
import shutil
import sys
import datetime

from invoke import task
from invoke.util import cd
from pelican.server import ComplexHTTPRequestHandler, RootedHTTPServer

CONFIG = {
    # Local path configuration (can be absolute or relative to tasks.py)
    'deploy_path': 'output',
    # Github Pages configuration
    'github_pages_branch': 'gh-pages',
    'commit_message': "'Publish site on {}'".format(datetime.date.today().isoformat()),
    # Port for `serve`
    'port': 8000,
    # Remote github page site
    'github_pages_repo': 'git@github.com:t-redactyl/t-redactyl.github.io.git',
    # Remote github page branch
    'github_pages_remote_branch': 'master',

    'site_domain': 't-redactyl.io'
}

@task
def clean(c):
    """Remove generated files"""
    if os.path.isdir(CONFIG['deploy_path']):
        shutil.rmtree(CONFIG['deploy_path'])
        os.makedirs(CONFIG['deploy_path'])

@task
def build(c):
    """Build local version of site"""
    c.run('pelican -s pelicanconf.py')

@task
def preview(c):
    """Build production version of site"""
    c.run('pelican -s publishconf.py')

@task
def publish(c):
    """Publish to GitHub Pages"""
    preview(c)
    c.run('ghp-import {deploy_path} -b {github_pages_branch} -c {site_domain}'.format(**CONFIG))
    c.run('git push -f {github_pages_repo} {github_pages_branch}:{github_pages_remote_branch}'.format(**CONFIG))

@task
def reserve(c):
    """ Automatically reload and serve changes"""
    c.run('pelican --listen --autoreload')
