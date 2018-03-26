# VMaaS tests

## Setup

* install and setup VMaaS following instructions in [VMaaS README](https://github.com/RedHatInsights/vmaas/blob/master/README.md)
* create new python virtual environment using ``virtualenv -p python3 .vmaas_venv``
* activate the environment using ``. vmaas_venv/bin/activate``
* install tests requirements using ``pip install -r requirements.txt``

## Running tests

```
pytest -v
```
