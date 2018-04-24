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

```bash
pytest -v
```

## Perf tests

Install [tsung](http://tsung.erlang-projects.org/) testing tool (``dnf install tsung`` on Fedora).

Run tests using ``run_upload_perf_test.py`` script.

This will run perf tests for 60 seconds with 50 concurrent users and with 300 packages per request randomly selected from packages list agains VMaaS server running on localhost port 8080:

```bash
vmaas/scripts/run_upload_perf_test.py -i rpm_list.txt -p 300 -s localhost:8080 -d 60 -u 50
```
