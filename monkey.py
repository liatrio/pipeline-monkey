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

def parse_repo_config(repo):
    repo_config = next((rc for rc in MONKEY_CONFIG['repos'] if rc['name'] == repo), None)
    if repo_config is None:
        raise ValueError('Git repo {} is not configured'.format(repo))
    else:
        return repo_config

@click.group()
@click.option('--log-level', help='Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)')
@click.option('--log-file', help='Path to log file.')
def cli(log_level, log_file):
    # Parse logging config
    log_level = log_level or MONKEY_CONFIG.get('log_level', None) or 'INFO'
    log_file = log_file or MONKEY_CONFIG.get('log_file', None) 

    # Setup logging
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
@click.argument('repo', nargs=1)
@click.option('--branch', default='master', help='Branch to commit in (default master)')
@click.option('--count', default='1', help='Maximum number of commits to push (default 1).')
@click.option('--interval', default='5', help='Interval between commits in minutes (default 1). Provide a range (X,Y) to wait a random amount of time between commits')
@click.option('--timeout', default='60', help='Maximum amount of time (minutes) to commit before exiting (default 60)')
def commit(repo, branch, count, interval, timeout):
    startime = datetime.now()
    total_commits = 0

    try:
        repo_config = parse_repo_config(repo)
    except ValueError as e:
        logger.error(e)
        exit(1)

    def stoptime_reached():
        return timeout and (datetime.now() > (startime + timedelta(minutes=int(timeout))))

    def commit_count_reached():
        return total_commits >= int(count)

    def should_terminate():
        return stoptime_reached() or commit_count_reached()

    def start_message():
        logger.debug('Starting autocommit sequence.')
        logger.debug('Committing to {} on branch {} every {} minutes up to {} commits or until timeout is reached in {} minutes'.format(repo, branch, interval, count, timeout))

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
        push_empty_commit(repo_config['path'], branch=branch)
        logger.info('Pushed empty commit to {}-{}'.format(repo, branch))
        total_commits += 1
        if should_terminate():
            break
        else:
            wait()

    summary()

@cli.command('generate', help='Generate jobs from predefined templates')
@click.argument('repo', nargs=1)
@click.option('--branch', default='master', help='Branch to poll in job(s)')
@click.option('--count', default=1, help='Number of jobs to make (per repo)')
def generate(repo, branch, count):
    count = int(count)

    try:
        repo_config = parse_repo_config(repo)
    except ValueError as e:
        logger.error(e)
        exit(1)

    def handle_maven():
        goal = repo_config.get('goal', 'test')
        generate_maven_jobs(repo_config['name'], repo_config['url'], branch, count, goal)
        logger.info('Generated {} job(s) for {} {}'.format(count, repo, branch))

    if repo_config['job_template'] == 'maven':
        handle_maven()


@cli.command('clean', help='Delete generated jobs from Jenkins')
@click.option('--repo', help='Delete jobs only for a specific repo')
@click.option('--branch', help='Delete jobs for only a specific branch (must also specify repo)')
def delete_jobs(repo=None, branch=None):
    clean(repo, branch)

if __name__ == '__main__':
    cli()

