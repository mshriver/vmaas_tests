# VMaaS tests

## Setup

* install and setup VMaaS following instructions in [VMaaS README](https://github.com/RedHatInsights/vmaas/blob/master/README.md)
* import repositories data
* create new python virtual environment using ``virtualenv -p python3 .vmaas_venv``
* activate the environment using ``. vmaas_venv/bin/activate``
* install tests requirements using ``pip install -r requirements.txt``


## DB setup (requires additional configuration files)

* clone repository with config files
* change directory to `vmaas_tests`
* setup the DB using the following
```
vmaas/scripts/setup_db.sh <path_to_repolist> <target_hostname> <path_to_vmaas_project>
```
* or more specifically
```
vmaas/scripts/setup_db.sh ../vmaas-yamls/data/repolist.json localhost ../vmaas
```


## Running tests

```
$ pytest -v
```
