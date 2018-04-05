# -*- coding: utf-8 -*-

import os

import pytest

from vmaas.rest.client import VMaaSClient
from vmaas.utils.conf import conf as _conf

CONF_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', '..', 'conf')

# TODO: initialize logging


@pytest.fixture()
def conf():
    return _conf


@pytest.fixture()
def rest_api(conf):
    hostname = conf.get('hostname', 'localhost')
    return VMaaSClient(hostname)
