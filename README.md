# Pipeline Monkey

A command line tool for simulating developer activity in a CI pipeline.

## Features:

* **Automatic Commits** - Automatically push commits to remote repos on an interval.
* **Job Generation** - Bulk create jobs remotely from predefined job templates.
* **Custom Job Templates** - Define your own job templates to be use by the job generator **(coming soon)**.
* **Activity Simulator** - Randomly push commits and create jobs for many different repos to simulate realistic development activity. **(coming soon)**.

## Configuration

Create a file **config.json** in your working directory with the following format:

```js
{
  "jenkins_url": "jenkins.example.com:8080"
  "jenkins_user": "<jenkins-user>"
  "jenkins_token": "<jenkins-api-token>",
  "log_level": "INFO",
  "log_file": "./monkey.log",
  "repos": [
    {
      "url": "git@github.com:ebracho/spring-petclinic.git",
      "job_template": "maven",
      "goal": "test"
    }
  ]
}
```

* **jenkins_url** - Url to the jenkins server to generate jobs on 
* **jenkins_user** - User to login as on Jenkins server
* **jenkins_token** - Token to authenticate with jenkins server. Retrieve this at http://<jenkins_url>/users/<user>/configure
* **log_level** (optional) - Set to DEBUG, INFO, WARNING, ERROR, CRITICAL. Defaults to INFO
* **log_file** (optional) - Path to log file. Defaults to stdout
* **repos**
  * **url** - Url reference to the repo (prefer ssh over https). You must have some form of passwordless authentication setup (See https://github.com/saga-project/BigJob/wiki/Configuration-of-SSH-for-Password-less-Authentication). 
  * **job_template** - Job dsl template to use when generating jobs for this repo/branch. See **Job Templates** below.
  * **job-specific-attributes** - Depending on the job template, there may be more job-specific parameters to provice (like *goal* in this example). See **Job Templates** below.

## Jenkins Plugins
Pipeline Monkey expects the following plugins to be installed on the Jenkins instance:
* [Job DSL Plugin](https://wiki.jenkins-ci.org/display/JENKINS/Job+DSL+Plugin)
* [Cloudbees Folder Plugin](https://wiki.jenkins-ci.org/display/JENKINS/CloudBees+Folders+Plugin)
* [Maven Project Plugin](https://wiki.jenkins-ci.org/display/JENKINS/Maven+Project+Plugin)

## Running

### Virtualenv
1. Install Python 3.5 or later on your system. See https://www.python.org/downloads/
2. Install virtualenv. `pip install virtualenv`
3. Create a virtualenv for pipeline monkey. `virtualenv -p /path/to/python3.5 venv`
4. Activate the virtualenv. `source venv/bin/activate`
5. Install the Pipeline Monkey dependencies. `pip install -r requirements.txt`
6. Test that everything works. `./monkey.py --help`

### Docker

TODO

## CLI

### Commit
```
Usage: monkey commit [OPTIONS] REPO

  Automatically commit and push changes to git repositories.

Options:
  --branch TEXT    Branch to commit in (default master)
  --count TEXT     Maximum number of commits to push (default 1).
  --interval TEXT  Interval between commits in minutes (default 1). Provide a
                   range (X,Y) to wait a random amount of time between commits
  --timeout TEXT   Maximum amount of time (minutes) to commit before exiting
                   (default 60)
  --help           Show this message and exit.
```
**Example**: `monkey commit spring-petclinic --branch master --interval 10,20 --count 10 --timeout 180` - Pushes empty commits to the spring-petclinic remote on random intervals between 10-20 minutes. Terminates after 10 commits or after 180 minutes.

### Generate
```
Usage: monkey generate [OPTIONS] REPO

  Generate jobs from predefined templates

Options:
  --branch TEXT    Branch to poll in job(s)
  --count INTEGER  Number of jobs to make (per repo)
  --help           Show this message and exit.
```
**Example**: `monkey generate spring-petclinic --branch master --count 25` - Generates 25 jobs that poll the spring-petclinic master branch. Generated jobs will be located in the *pipeline-monkey* job folder.

### Clean
```
Usage: monkey clean [OPTIONS]

  Delete generated jobs from Jenkins

Options:
  --repo TEXT    Delete jobs only for a specific repo
  --branch TEXT  Delete jobs for only a specific branch (must also specify
                 repo)
  --help         Show this message and exit.
```
**Example**: `monkey clean --repo spring-petclinic --branch master` - Deletes all generated jobs for the spring-petclinic master branch.


## Job Templates

### Maven

Creates a basic Maven job that polls scm and executes the specified goal. 

#### Parameters

* **goal** - Maven goal to execute (validate, compile, test, package, verify, install or deploy)

