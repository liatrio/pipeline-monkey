#!/usr/bin/env python3

#
# CLI 
#

import time
from datetime import datetime, timedelta
import random
import sys
import click
from config import MONKEY_CONFIG
from commit import push_empty_commit
from jenkins_jobs import generate_maven_jobs, clean

def parse_repos(repos):
    """
    Parse and retrieve configs for a comma-seperated list of repos.
    If list is empty, return all repo configs
    """
    if not repos:
        yield from MONKEY_CONFIG['repos']
    else:
        for repo in repos.split(','):
            repo_config = next((rc for rc in MONKEY_CONFIG['repos'] if rc['name'] == repo), None)
            if not repo_config:
                click.secho('Unknown repo {}'.format(repo), fg='red')
                exit(1)
            else:
                yield repo_config

@click.group()
def cli():
    pass

@cli.command('commit', help='Automatically commit and push changes to git repositories.')
@click.option('--count', default=1, help='Number of commits to apply')
@click.option('--repos', help='Comma-seperated list of repos to create commits in')
@click.option('--interval', default='5', help='Interval between commits (minutes). Provide a range (X,Y) to wait a random amount of time between commits')
@click.option('--timeout', default='60', help='Maximum amount of time (minutes) to commit before exiting')
def commit(count, repos, interval, timeout):
    stopping_time = datetime.now() + timedelta(minutes=int(timeout))

    # Parse interval and build wait function
    def wait():
        """
        Waits for next commit based on interval. Returns True if timed out.
        """
        if ',' in interval:
            waittime = int(random.uniform(*map(int,interval.split(',')))*60)
        else:
            waittime = int(interval)*60
        if (datetime.now() + timedelta(seconds=waittime)) > stopping_time:
            return True
        click.echo('Waiting {} seconds until next round of commits'.format(waittime))
        time.sleep(waittime)

    # Push commits on interval
    repo_configs = list(parse_repos(repos))
    for i in range(count):
        if i > 0:
            if wait():
                click.secho('Timeout reached. Aborting', fg='green')
                return
        for rc in repo_configs:
            click.secho('Pushing empty commit in {}'.format(rc['name']), fg='green')
            push_empty_commit(rc['path'], rc.get('remote', 'origin'), rc.get('branch', 'master'))

    click.echo('Finished pushing commits')

@cli.command('generate-jobs', help='Generate jobs from predefined templates')
@click.option('--repos', help='Comma-seperated list of repos to generate jobs for')
@click.option('--count', default=1, help='Number of jobs to make (per repo)')
def generate_jobs(repos, count):
    repo_configs = parse_repos(repos)
    for repo_config in repo_configs:
        if repo_config['job_template'] == 'maven':
            goal = repo_config.get('goal', None)
            if not goal:
                click.secho('Goal must be specified for maven job ({})'.format(repo_config['name']), fg='red')
                exit(1)
            else:
                generate_maven_jobs(repo_config['name'], repo_config['url'], 
                    repo_config.get('branch', 'master'), count, goal)
                click.secho('Generated {} jobs for {}'.format(count, repo_config['name']), fg='green')

@cli.command('delete-jobs', help='Delete generated jobs from Jenkins')
@click.option('--repos', help='Comma seperated list of repos from which to delete jobs (default all repos)')
def delete_jobs(repos):
    if not repos:
        clean()
    else:
        all(parse_repos(repos))
        clean(repos)


if __name__ == '__main__':
    cli()

