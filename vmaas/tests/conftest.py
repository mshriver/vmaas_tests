# -*- coding: utf-8 -*-

import logging

import pytest

from vmaas.rest.client import VMaaSClient
from vmaas.utils.conf import conf


logging.basicConfig()


@pytest.fixture()
def rest_api():
    hostname = conf.get('hostname', 'localhost')
    return VMaaSClient(hostname)
