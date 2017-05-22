#
# Functions for pushing commits to git repos
#

import os
import datetime
import git

def push_empty_commit(repo_path, remote='origin', branch='master'):
    """
    Adds a timestamp to the repo's monkey.log file and commits/pushes to specified branch
    """
    repo = git.Repo(repo_path)
    repo.git.checkout(branch)
    logfile = os.path.join(repo_path, 'monkey.log')
    timestamp = datetime.datetime.now().strftime('%c')
    logentry = 'Empty Commit - {}'.format(timestamp)
    with open(logfile, 'a') as f:
        print(logentry, file=f)
    repo.git.add(logfile)
    repo.git.commit(logfile, m=logentry)
    repo.git.push(remote, branch)

