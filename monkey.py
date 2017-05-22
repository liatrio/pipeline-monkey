#!/usr/bin/env python3

#
# CLI 
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
    # Parse interval and build wait function
    def wait():
        if ',' in interval:
            waittime = random.randrange(*interval.split(',').map(int))*60
        else:
            waittime = int(interval)*60
        click.echo('Waiting {} seconds until next round of commits'.format(waittime))
        time.sleep(waittime)

    # Parse and lookup repos
    def parse_repos():
        if repos is None:
            yield from MONKEY_CONFIG['repos']
        else:
            for repo in repos.split(','):
                repo_config = next((rc for rc in MONKEY_CONFIG['repos'] if rc['name'] == repo), None)
                if not repo_config:
                    click.secho('Unknown repo {}'.format(repo), fg='red')
                    exit(1)
                else:
                    yield repo_config
            
    # Push commits on interval
    repo_configs = list(parse_repos())
    for i in range(count):
        if i > 0:
            wait()
        for rc in repo_configs:
            click.secho('Pushing empty commit in {}'.format(rc['name']), fg='green')
            push_empty_commit(rc['path'], rc.get('remote', 'origin'), rc.get('branch', 'master'))

    click.echo('Finished pushing commits')



def create_build_job():
    pass

if __name__ == '__main__':
    cli()

