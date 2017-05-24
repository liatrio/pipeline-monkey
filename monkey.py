#!/usr/bin/env python3

#
# CLI 
#

import time
from datetime import datetime, timedelta
import random
import sys
import logging
import click
from config import MONKEY_CONFIG
from commit import push_empty_commit
from jenkins_jobs import generate_maven_jobs, clean

logger = logging.getLogger('pipeline_monkey')

def parse_repos(repos):
    """
    Parse a comma-seperated list of repos and return their configs
    If list is empty, return all repo configs
    """
    if not repos:
        yield from MONKEY_CONFIG['repos']
    else:
        for repo in repos.split(','):
            repo_config = next((rc for rc in MONKEY_CONFIG['repos'] if rc['name'] == repo), None)
            if not repo_config:
                logger.error('Unknown repo {}'.format(repo))
                exit(1)
            else:
                yield repo_config

@click.group()
@click.option('--log-level', default='DEBUG', help='Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)')
@click.option('--log-file', help='Path to log file.')
def cli(log_level, log_file):
    log_level = logging.getLevelName(log_level.upper())
    logger.setLevel(log_level)
    formatter = logging.Formatter('[%(asctime)s-%(levelname)s] %(message)s')
    if log_file:
        handler = logging.FileHandler(log_file)
    else:
        handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger.addHandler(handler)


@cli.command('commit', help='Automatically commit and push changes to git repositories.')
@click.option('--count', default='1', help='Maximum number of commits to push (default 1).')
@click.option('--repos', help='Comma-seperated list of repos to create commits in')
@click.option('--interval', default='5', help='Interval between commits in minutes (default 1). Provide a range (X,Y) to wait a random amount of time between commits')
@click.option('--timeout', default='60', help='Maximum amount of time (minutes) to commit before exiting (default 60)')
def commit(count, repos, interval, timeout):
    startime = datetime.now()
    total_commits = 0
    repo_configs = list(parse_repos(repos))

    def stoptime_reached():
        return timeout and (datetime.now() > (startime + timedelta(minutes=int(timeout))))

    def commit_count_reached():
        return total_commits >= int(count)

    def should_terminate():
        return stoptime_reached() or commit_count_reached()

    def start_message():
        repo_names = ','.join(map(lambda rc: rc['name'], repo_configs))
        logger.debug('Starting autocommit sequence.')
        logger.debug('Committing to {} every {} minutes up to {} commits or until timeout is reached in {} minutes'.format(repo_names, interval, count, timeout))

    def summary():
        if commit_count_reached():
            logger.debug('Terminating (commit count reached)')
        else:
            logger.debug('Terminating (timeout reached)')
        runtime = (datetime.now() - startime)
        if runtime.seconds <  300:
            logger.debug('{} commits pushed in {} seconds'.format(total_commits, runtime.seconds))
        else:
            logger.debug('{} commits pushed in {} minutes'.format(total_commits, runtime.seconds/60))

    def wait():
        """
        Waits for next commit based on interval. Returns True if stopping_time reached
        """
        if ',' in interval:
            waittime = int(random.uniform(*map(int,interval.split(',')))*60)
        else:
            waittime = int(interval)*60
        logger.debug('Waiting {} seconds until next round of commits'.format(waittime))
        time.sleep(waittime)

    start_message()

    # Push commits on interval
    while True:
        for rc in repo_configs:
            push_empty_commit(rc['path'], rc.get('remote', 'origin'), rc.get('branch', 'master'))
            logger.info('Pushed empty commit to {}'.format(rc['name']))
        total_commits += 1
        if should_terminate():
            break
        else:
            wait()

    summary()

@cli.command('generate-jobs', help='Generate jobs from predefined templates')
@click.option('--repos', help='Comma-seperated list of repos to generate jobs for')
@click.option('--count', default=1, help='Number of jobs to make (per repo)')
def generate_jobs(repos, count):
    repo_configs = parse_repos(repos)
    for repo_config in repo_configs:
        if repo_config['job_template'] == 'maven':
            goal = repo_config.get('goal', None)
            if not goal:
                logger.warning('Goal must be specified for maven job ({})'.format(repo_config['name']))
                exit(1)
            else:
                generate_maven_jobs(repo_config['name'], repo_config['url'], 
                    repo_config.get('branch', 'master'), count, goal)
                logger.info('Generated {} jobs for {}'.format(count, repo_config['name']))

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

