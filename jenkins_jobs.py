#
# Functions for creating Jenkins jobs through the Jenkins remote api
#

import os
import jenkins
from jinja2 import Template
from config import MONKEY_CONFIG, MONKEY_ROOT

server = jenkins.Jenkins(MONKEY_CONFIG['jenkins_url'], 
        username=MONKEY_CONFIG['jenkins_user'], 
        password=MONKEY_CONFIG['jenkins_token'])

def escape_xml(s):
    entities = [
      ('<', '&lt;'),
      ('>', '&gt;'),
      ('&', '&amp;'),
      ("'", '&apos;'),
      ('"', '&quot;'),
    ]
    for token, escaped in entities:
        s = s.replace(token, escaped)
    return s

def load_template(template_name):
    """
    Load a job template from the job_templates directory.
    """
    template_path = os.path.join(MONKEY_ROOT, 'templates', '{}.jinja2'.format(template_name))
    with open(template_path) as f:
        return Template(f.read())

def execute_seed_job(job_dsl):
    """
    Creates and executes a seed job with the provided job dsl
    """
    seedjob_config_template = load_template('xml/seedjob')
    params = {
        'escaped_dsl_script': escape_xml(job_dsl)
    }
    seedjob_config = seedjob_config_template.render(**params)
    if server.job_exists('pipeline-monkey-seedjob'):
        server.delete_job('pipeline-monkey-seedjob')
    server.create_job('pipeline-monkey-seedjob', seedjob_config)
    server.build_job('pipeline-monkey-seedjob')

def generate_maven_jobs(repo_name, repo_url, branch, job_count, goal):
    """
    Generates maven jobs in the pipeline-monkey folder
    """
    maven_dsl_template = load_template('groovy/maven')
    params = {
        'repo_name': repo_name,
        'repo_url':  repo_url,
        'branch':    branch,
        'job_count': job_count,
        'goal':      goal,
    }
    job_dsl = maven_dsl_template.render(**params)
    execute_seed_job(job_dsl)

def clean(repo=None, branch=None):
    """
    Delete generated for a specified repo/branch. 
    If no branch is specified, all jobs for all branches are deleted
    If no repo is specified, all jobs for all repos/branches are deleted
    Also deletes the seed job if it exists
    """
    if repo:
        if branch:
            folder = 'pipeline-monkey/{}'.format(repo)
        else:
            folder = 'pipeline-monkey/{}/{}'.format(repo, branch)
    else:
        folder = 'pipeline-monkey'

    if server.job_exists(folder):
        server.delete_job(folder)

    if server.job_exists('pipeline-monkey-seedjob'):
        server.delete_job('pipeline-monkey-seedjob')

