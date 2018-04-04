# -*- coding: utf-8 -*-

import pytest

from vmaas.rest import tools

CVES = [
    'CVE-2016-0634',
    'CVE-2016-7543',
]

EXPECTED_KEYS = [
    'impact',
    'description',
    'redhat_url',
    'cwe_list',
]


def check_keys(cve):
    for key in EXPECTED_KEYS:
        assert cve[key] is not None, 'Expected key `{}` has no value'.format(key)


class TestCVEsQuery(object):
    def test_post_multi(self, rest_api):
        """Tests multiple CVEs using POST."""
        request_body = tools.cves_body(CVES)
        cves = rest_api.get_cves(body=request_body).response_check()
        assert len(cves) == len(CVES)
        for cve_name in CVES:
            assert cve_name in cves
            check_keys(cves[cve_name])

    @pytest.mark.parametrize('cve_name', CVES)
    def test_post_single(self, rest_api, cve_name):
        """Tests single CVE using POST."""
        request_body = tools.cves_body([cve_name])
        cves = rest_api.get_cves(body=request_body).response_check()
        assert len(cves) == 1
        cve, = cves
        assert cve.name == cve_name
        check_keys(cve)

    @pytest.mark.parametrize('cve_name', CVES)
    def test_get(self, rest_api, cve_name):
        """Tests single CVE using GET."""
        cves = rest_api.get_cve(cve_name).response_check()
        assert len(cves) == 1
        cve, = cves
        assert cve.name == cve_name
        check_keys(cve)
