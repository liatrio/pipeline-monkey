#!/usr/bin/env python3

#
# CLI script for Pipeline Monkey
#

import click
from config import MONKEY_ROOT, MONKEY_CONFIG
from commit import get_repos, push_empty_commit

@click.group()
def cli():
    pass

@cli.command()
@click.option('--repos-dir', default=MONKEY_CONFIG['repos-dir'], help='Path to git repos directory')
@click.option('--count', default=1, help='Number of commits to apply')
@click.option('--repos', help='Repos to create commits in (default all)')
def commit(repos_dir, count, repos):
    if not repos:
        repos = get_repos(repos_dir)
    else:
        repos = repos.split()
    for repo_name in repos:
        for _ in range(count):
            push_empty_commit(repos_dir, repo_name)

def create_build_job():
    pass

def trigger_build_job():
    pass

if __name__ == '__main__':
    cli()

