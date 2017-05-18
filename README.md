## Pipeline Monkey

A tool for exercising CI pipelines.

### Features:

* Commit and push changes to git repos (coming soon)
* Create and trigger Jenkins build jobs (coming soon)

### Configuration

Configuration goes in *config.json*

* *repos_dir* - Path to directory containing git repositories. Commits will be added and pushed from these repos.
* *jenkins_url* - Url to the jenkins instance being exercised. Jobs will be created and triggered here.
* *jenkins_user* - Username to authenticate with Jenkins.
* *jenkins_token* - Token to authenticate with Jenkins.

### Contributint

#### Tests

Tests are located in the *test/* directory. Run tests with `nosetests`. 

