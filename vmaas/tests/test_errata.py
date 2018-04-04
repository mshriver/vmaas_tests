# -*- coding: utf-8 -*-

import pytest

from vmaas.rest import tools

ERRATA = [
    'RHBA-2016:2858',
    'RHSA-2017:1931',
]

EXPECTED_KEYS = [
    'updated',
    'description',
    'issued',
    'package_list',
    'cve_list',
    'severity',
    'url',
    'type',
]


def check_keys(erratum):
    for key in EXPECTED_KEYS:
        assert erratum[key] is not None, 'Expected key `{}` has no value'.format(key)


class TestErrataQuery(object):
    def test_post_multi(self, rest_api):
        """Tests multiple errata using POST."""
        request_body = tools.errata_body(ERRATA)
        errata = rest_api.get_errata(body=request_body).response_check()
        assert len(errata) == len(ERRATA)
        for erratum_name in ERRATA:
            assert erratum_name in errata
            check_keys(errata[erratum_name])

    @pytest.mark.parametrize('erratum_name', ERRATA)
    def test_post_single(self, rest_api, erratum_name):
        """Tests single erratum using POST."""
        request_body = tools.errata_body([erratum_name])
        errata = rest_api.get_errata(body=request_body).response_check()
        assert len(errata) == 1
        erratum, = errata
        assert erratum.name == erratum_name
        check_keys(erratum)

    @pytest.mark.parametrize('erratum_name', ERRATA)
    def test_get(self, rest_api, erratum_name):
        """Tests single erratum using GET."""
        errata = rest_api.get_erratum(erratum_name).response_check()
        assert len(errata) == 1
        erratum, = errata
        assert erratum.name == erratum_name
        check_keys(erratum)
