#!/usr/bin/env python3

#
# CLI script for Pipeline Monkey
#

import time
import random
import click
from config import MONKEY_ROOT, MONKEY_CONFIG
from commit import get_repos, push_empty_commit

@click.group()
def cli():
    pass

@cli.command()
@click.option('--repos-dir', default=MONKEY_CONFIG['repos-dir'], help='Path to git repos directory')
@click.option('--count', default=1, help='Number of commits to apply')
@click.option('--repos', help='Comma-seperated list of repos to create commits in (default all)')
@click.option('--interval', default='5', help='Interval between commits (minutes). Provide a range (X,Y) to wait a random amount of time between commits')
def commit(repos_dir, count, repos, interval):
    if not repos:
        repos = get_repos(repos_dir)
    else:
        repos = repos.split(',')
    if ',' in interval:
        l,u = map(int, interval.split(','))
        get_wait_period = lambda: random.randrange(l*60,u*60)
    else:
        get_wait_period = lambda: int(interval)*60
    for _ in range(count-1):
        for repo_name in repos:
            push_empty_commit(repos_dir, repo_name)
        wait_period = get_wait_period()
        click.echo("Waiting {} seconds for next round of commits".format(wait_period))
        time.sleep(wait_period)
    for repo_name in repos:
        push_empty_commit(repos_dir, repo_name)


def create_build_job():
    pass

def trigger_build_job():
    pass

if __name__ == '__main__':
    cli()

