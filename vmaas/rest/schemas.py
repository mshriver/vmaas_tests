# -*- coding: utf-8 -*-
"""
Schemas of responses.
"""

from schema import Optional, Schema


_cves = {
    'cve_list': {
        str: {
            'impact': str,
            'public_date': str,
            'synopsis': str,
            'description': str,
            'modified_date': str,
            Optional('redhat_url'): str,
            'cvss3_score': str,
            Optional('secondary_url'): str,
            'cwe_list': [str],
        }
    }
}

_errata = {
    'errata_list': {
        str: {
            'updated': str,
            'severity': str,
            'reference_list': [str],
            'issued': str,
            'description': str,
            'solution': str,
            'summary': str,
            'url': str,
            'synopsis': str,
            'cve_list': [str],
            'bugzilla_list': [str],
            'package_list': [str],
            'type': str,
        }
    }
}

_repos = {
    'repository_list': {
        str: [
            {
                'product': str,
                'releasever': str,
                'name': str,
                'url': str,
                'basearch': str,
                'revision': str,
                'label': str,
            }
        ]
    }
}

_updates_top = {'update_list': {str: dict}}
_updates_top_repolist = {'repository_list': [str], 'update_list': {str: dict}}

_updates_package = {
    'available_updates': [
        {
            'basearch': str,
            'erratum': str,
            'releasever': str,
            'repository': str,
            'package': str,
        }
    ],
    'description': str,
    'summary': str,
}

cves_schema = Schema(_cves)
errata_schema = Schema(_errata)
repos_schema = Schema(_repos)
updates_top_schema = Schema(_updates_top)
updates_top_repolist_schema = Schema(_updates_top_repolist)
updates_package_schema = Schema(_updates_package)
