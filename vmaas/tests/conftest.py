# -*- coding: utf-8 -*-

import os
import logging

import pytest
import yaml

from vmaas.rest.client import VMaaSClient

CONF_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', '..', 'conf')

# TODO: initialize logging


@pytest.fixture()
def conf():
    """Loads config file and returns its content."""
    default_conf = os.path.join(CONF_PATH, 'env.yaml')
    local_conf = os.path.join(CONF_PATH, 'env.local.yaml')

    try:
        with open(local_conf):
            pass
    except EnvironmentError:
        local_conf = None

    with open(default_conf, encoding='utf-8') as input_file:
        config_settings = yaml.load(input_file)
    logging.debug('Default config loaded from `{}`'.format(default_conf))

    if local_conf:
        with open(local_conf, encoding='utf-8') as input_file:
            config_settings_user = yaml.load(input_file)
        logging.info('Config loaded from `{}`'.format(local_conf))

        # merge default and user configuration
        config_settings.update(config_settings_user)

    return config_settings


@pytest.fixture()
def rest_api(conf):
    hostname = conf.get('hostname', 'localhost')
    return VMaaSClient(hostname)
