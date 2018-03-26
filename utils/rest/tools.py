# -*- coding: utf-8 -*-
"""
REST API helper functions
"""

import datetime


def cves_body(cves):
    return dict(cve_list=cves)


def errata_body(errata):
    return dict(errata_list=errata)


def repos_body(repos):
    return dict(repository_list=repos)


def updates_body(packages, repositories=None, modified_since=None):
    body = dict(package_list=packages)
    if repositories:
        body['repository_list'] = repositories
    if modified_since:
        if isinstance(modified_since, datetime.datetime):
            modified_since = modified_since.replace(microsecond=0).isoformat()
        body['modified_since'] = modified_since
    return body
