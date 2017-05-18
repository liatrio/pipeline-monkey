#
# Functions for listing, commiting and pushing from configured git repos
#

import os
import subprocess
import datetime

from execute import execute_shell, execute_shell_with_output

def get_repos(repos_dir):
    """
    Return a list of repos found in the `repos_dir` config attribute.
    """
    res = execute_shell('ls {}'.format(repos_dir))
    return res.split()

def push_empty_commit(repos_dir, repo_name):
    """
    Pushes an empty commit to the default upstream of a repo,
    Adds a timestamped message to the monkey.log file of the repo
    """
    if not repo_name in get_repos(repos_dir):
        raise ValueError('repository {} not found in repos dir ({})'.format(repo_name, repos_dir))
    repo = os.path.join(repos_dir, repo_name)
    time = datetime.datetime.now().strftime('%c')
    script = """
    echo Empty Commit - {time} >>{repo}/monkey.log;
    git -C {repo} add {repo}/monkey.log;
    git -C {repo} commit -m "Pipeline Monkey - {time}";
    git -C {repo} push;
    """.format(repo=repo, time=time)
    return execute_shell_with_output(script, 'Pushing empty commit to {}'.format(repo_name))

