## Pipeline Monkey

A tool for exercising CI pipelines.

### Features:

* Commit and push changes to git repos (coming soon)
* Create and trigger Jenkins build jobs (coming soon)

### Setup

* Create a [virtualenv](http://python-guide-pt-br.readthedocs.io/en/latest/dev/virtualenvs/) with python3.5: `virtualenv -p <path/to/python3.5> venv; source venv/bin/activate`
* `pip install -r requirement.txt`
* Create a directory containing  git repos for Pipeline Monkey to commit/push to.
* Edit config.json (see next section)

### Configuration

Configuration goes in *config.json*

* *repos_dir* - Path to directory containing git repositories. Commits will be added and pushed from these repos.
* *jenkins_url* - Url to the jenkins instance being exercised. Jobs will be created and triggered here.
* *jenkins_user* - Username to authenticate with Jenkins.
* *jenkins_token* - Token to authenticate with Jenkins.


### Contributing

#### Tests

Tests are located in the *test/* directory. Run tests with `nosetests`. 

