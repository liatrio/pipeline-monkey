#!/usr/bin/env python3

#
# CLI script for Pipeline Monkey
#

import time
import random
import sys
import click
from config import MONKEY_CONFIG
from commit import push_empty_commit

@click.group()
def cli():
    pass

@cli.command(help='Automatically commit and push changes to git repositories.')
@click.option('--count', default=1, help='Number of commits to apply')
@click.option('--repos', help='Comma-seperated list of repos to create commits in')
@click.option('--interval', default='5', help='Interval between commits (minutes). Provide a range (X,Y) to wait a random amount of time between commits')
def commit(count, repos, interval):
    # Parse interval and create wait function
    def wait():
        if ',' in interval:
            waittime = random.randrange(*interval.split(',').map(int))*60
        else:
            waittime = int(interval)*60
        click.echo('Waiting {} seconds until next round of commits'.format(waittime))
        time.sleep(waittime)

    # Parse repos
    if repos is None:
        repos = MONKEY_CONFIG['repos']
    else:
        repos = list(filter(lambda r: r['name'] in repos, MONKEY_CONFIG['repos']))

    # Push commits on interval
    for i in range(count):
        if i > 0:
            wait()
        for repo in repos:
            click.secho('Pushing empty commit in {}'.format(repo['name']), fg='green')
            push_empty_commit(repo['path'], repo.get('remote', 'origin'), repo.get('branch', 'master'))

    click.echo('Finished pushing commits')



def create_build_job():
    pass

def trigger_build_job():
    pass

if __name__ == '__main__':
    cli()

