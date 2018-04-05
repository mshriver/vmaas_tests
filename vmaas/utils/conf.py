# -*- coding: utf-8 -*-
"""
Configuration loading.
"""

import os

import yaml

CONF_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', '..', 'conf')


def get_conf():
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

    if local_conf:
        with open(local_conf, encoding='utf-8') as input_file:
            config_settings_user = yaml.load(input_file)

        # merge default and user configuration
        config_settings.update(config_settings_user)

    return config_settings


conf = get_conf()
