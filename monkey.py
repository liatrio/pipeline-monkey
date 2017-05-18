#!/usr/bin/env python3

import os
import subprocess
import datetime
import json

from execute import execute_shell

root_dir = os.path.dirname(os.path.realpath(__file__))

with open(os.path.join(root_dir, 'config.json')) as f:
    config = json.load(f)

def get_repos():
    res = subprocess.run(['ls', config['repos_dir']], stdout=subprocess.PIPE)
    return res.stdout.decode('utf-8').split()

def push_empty_commit(repo):
    repo = os.path.join(config['repos_dir'], repo)
    time = datetime.datetime.now().strftime('%c')
    script = """
    echo Empty Commit - {time} >>{repo}/monkey.log;
    git -C {repo} add {repo}/monkey.log;
    git -C {repo} commit -m "Pipeline Monkey - {time}";
    git -C {repo} push;
    """.format(repo=repo, time=time)
    return execute_shell(script, 'Pushing empty commit to {}'.format(repo))

