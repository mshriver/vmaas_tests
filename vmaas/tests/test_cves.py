# -*- coding: utf-8 -*-

import pytest

from vmaas.rest import schemas, tools

CVES = [
    'CVE-2016-0634',
    'CVE-2016-7543',
]


class TestCVEsQuery(object):
    def test_post_multi(self, rest_api):
        """Tests multiple CVEs using POST."""
        request_body = tools.gen_cves_body(CVES)
        cves = rest_api.get_cves(body=request_body).response_check()
        schemas.cves_schema.validate(cves.raw.body)
        assert len(cves) == len(CVES)
        for cve_name in CVES:
            assert cve_name in cves

    @pytest.mark.parametrize('cve_name', CVES)
    def test_post_single(self, rest_api, cve_name):
        """Tests single CVE using POST."""
        request_body = tools.gen_cves_body([cve_name])
        cves = rest_api.get_cves(body=request_body).response_check()
        schemas.cves_schema.validate(cves.raw.body)
        assert len(cves) == 1
        cve, = cves
        assert cve.name == cve_name

    @pytest.mark.parametrize('cve_name', CVES)
    def test_get(self, rest_api, cve_name):
        """Tests single CVE using GET."""
        cves = rest_api.get_cve(cve_name).response_check()
        schemas.cves_schema.validate(cves.raw.body)
        assert len(cves) == 1
        cve, = cves
        assert cve.name == cve_name
