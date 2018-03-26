# -*- coding: utf-8 -*-

import pytest

from utils.rest import tools

ERRATAS = [
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


class TestErratasQuery(object):
    def test_post_multi(self, rest_api):
        """Tests multiple errata using POST."""
        request_body = tools.errata_body(ERRATAS)
        errata = rest_api.get_errata(body=request_body).response_check()
        assert len(errata) == len(ERRATAS)
        for errata_name in ERRATAS:
            assert errata_name in errata
            check_keys(errata[errata_name])

    @pytest.mark.parametrize('errata_name', ERRATAS)
    def test_post_single(self, rest_api, errata_name):
        """Tests single erratum using POST."""
        request_body = tools.errata_body([errata_name])
        errata = rest_api.get_errata(body=request_body).response_check()
        assert len(errata) == 1
        erratum, = errata
        assert erratum.name == errata_name
        check_keys(erratum)

    @pytest.mark.parametrize('errata_name', ERRATAS)
    def test_get(self, rest_api, errata_name):
        """Tests single erratum using GET."""
        errata = rest_api.get_erratum(errata_name).response_check()
        assert len(errata) == 1
        erratum, = errata
        assert erratum.name == errata_name
        check_keys(erratum)
