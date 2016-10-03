from fabric.api import *
import os
import sys
import SocketServer
import pelicanconf
import publishconf
import coloredlogs, logging

from pelican.server import ComplexHTTPRequestHandler
from git import Repo, InvalidGitRepositoryError, NoSuchPathError

join = os.path.join
normpath = os.path.normpath


def full_path(x): return join(os.path.dirname(os.path.realpath(__file__)), x)

blog_path = os.path.dirname(os.path.realpath(__file__))
PORT = 8000 # Serve port

coloredlogs.install()


def clean(generated_path=pelicanconf.OUTPUT_PATH):
    """Remove generated files"""
    repo = Repo(blog_path)
    output_path = full_path(generated_path)

    if any(normpath(x.abspath) == normpath(output_path) for x in repo.submodules):
        logging.warn("Output directory is a git submodule, resetting it.")

        try:
            output_repo = Repo(output_path)
            output_repo.head.reset(working_tree=True, hard=True)
            output_repo.git.clean("-f")
        except NoSuchPathError:
            os.mkdir(generated_path)
            local("git submodule update --init")
    else:
        logging.warn("Output path is not a git submodule, deleting it.")
        local("rm -rf {0}".format(pelicanconf.OUTPUT_PATH))


def build():
    """Build local version of site"""
    local('pelican -s pelicanconf.py')


def rebuild():
    """`clean` then `build`"""
    clean()
    build()


def regenerate():
    """Automatically regenerate site upon file modification"""
    local('pelican -r -s pelicanconf.py')


def serve():
    """Serve site at http://localhost:8000/"""
    os.chdir(pelicanconf.OUTPUT_PATH)

    class AddressReuseTCPServer(SocketServer.TCPServer):
        allow_reuse_address = True

    server = AddressReuseTCPServer(('', PORT), ComplexHTTPRequestHandler)

    sys.stderr.write('Serving on port {0} ...\n'.format(PORT))
    server.serve_forever()


def reserve():
    """`build`, then `serve`"""
    build()
    serve()


def preview():
    """Build production version of site"""
    local('pelican -s publishconf.py')


def create_submodule():
    repo = Repo(blog_path)
    if not (repo.submodule(publishconf.SUBMODULE_NAME).module_exists()):
        logging.warn("Output submodule {0} doesn't exists, creating it at {1}.".format(
            publishconf.SUBMODULE_NAME, publishconf.OUTPUT_PATH))

        repo.create_submodule(url=publishconf.GITHUB_REPO, name=publishconf.SUBMODULE_NAME,
                              path=publishconf.OUTPUT_PATH, branch="master")

    repo.submodule_update(init=True)


def update_submodule():
    output_repo = Repo(full_path(publishconf.OUTPUT_PATH))
    output_repo.remote("origin").pull("master")

    repo = Repo(blog_path)
    if any(x for x in repo.index.diff(None) if normpath(x.a_path) == normpath(publishconf.OUTPUT_PATH)):
        logging.warn("Updating submodule to latest version")
        repo.git.add(publishconf.OUTPUT_PATH)
        repo.index.commit(message="Updated output to latest version in remote")


def push_changes():
    output_repo = Repo(full_path(publishconf.OUTPUT_PATH))

    if output_repo.is_dirty():
        # Adding untracked files
        output_repo.index.add(x for x in output_repo.untracked_files)

        # Adding modified files
        output_repo.index.add(x.a_path for x in output_repo.index.diff(None) if x.change_type == 'M')

        local("git --git-dir={0}/.git commit".format(output_repo.working_tree_dir))

        # Pushing output to master, publishing the blog
        output_repo.remote("origin").push("master")

    else:
        logging.info("No changes made to the blog!")


def publish():
    """Publish to production to github pages"""
    clean(generated_path=publishconf.OUTPUT_PATH)
    create_submodule()
    update_submodule()

    preview()

    push_changes()
    update_submodule()
