# -*- coding: utf-8 -*-
"""
REST API helper functions
"""

import datetime


def cves_body(cves):
    return dict(cve_list=cves)


def erratas_body(erratas):
    return dict(errata_list=erratas)


def updates_body(packages, repositories=None, modified_since=None):
    body = dict(package_list=packages)
    if repositories:
        body['repository_list'] = repositories
    if modified_since:
        if isinstance(modified_since, datetime.datetime):
            modified_since = modified_since.replace(microsecond=0).isoformat()
        body['modified_since'] = modified_since
    return body
