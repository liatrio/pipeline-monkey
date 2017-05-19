import os
import sys
import json
import git
import click

MONKEY_ROOT = os.path.dirname(os.path.realpath(__file__))
MONKEY_DOTDIR = os.path.join(MONKEY_ROOT, '.monkey')
MONKEY_REPOS = os.path.join(MONKEY_DOTDIR, 'repos')

os.makedirs(MONKEY_DOTDIR, exist_ok=True)  
os.makedirs(MONKEY_REPOS, exist_ok=True)  

def extract_remote_repo_name(repo_url):
    """
    Extract the name of the repo from its url
    """
    return os.path.splitext(os.path.basename(repo_url))[0]

def clone_repo(repo_url, root=MONKEY_REPOS, progress=None):
    """
    Idempotently clone a repo to the specified root directory (default MONKEY_ROOT/.monkey)
    Takes an optional progress argument (see http://gitpython.readthedocs.io/en/stable/reference.html#git.remote.Remote.push)
    """
    repo_name = extract_remote_repo_name(repo_url)
    repo_path = os.path.join(root, repo_name)
    if not os.path.isdir(repo_path):
        git.Repo.clone_from(repo_url, repo_path, progress)
    return (repo_name, repo_path)

# Load config
with open(os.path.join(MONKEY_ROOT, 'config.json')) as f:
    MONKEY_CONFIG = json.load(f)
    # Clone remote repos, derive repo names
    for repo in MONKEY_CONFIG['repos']:
        if 'path' not in repo:
            if 'url' not in repo:
                click.echos('Error: "path" or "url" attributes must be specified for repos', fg='red')
                sys.exit(1)
            repo['name'], repo['path'] = clone_repo(repo['url'])
            repo['remote'] = repo['url']
        else:
            repo['name'] = os.path.basename(repo['path'])

