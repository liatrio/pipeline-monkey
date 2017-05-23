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

def clean(repos=None):
    """
    Delete generated jobs for each repo (default all reapos).
    Also deletes the seed job if it exists
    """
    if type(repos) is str:
        repos = [repos]
    # Delete Repos
    if repos:
        for repo in repos:
            repo_folder = 'pipeline-monkey/{}'.format(repo)
            if server.job_exists(repo_folder):
                server.delete_job(repo_folder)
    else:
        if server.job_exists('pipeline-monkey'):
            server.delete_job('pipeline-monkey')
    # Delete seedjob
    if server.job_exists('pipeline-monkey-seedjob'):
        server.delete_job('pipeline-monkey-seedjob')

