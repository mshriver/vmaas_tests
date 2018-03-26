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


def check_keys(errata):
    for key in EXPECTED_KEYS:
        assert errata[key] is not None, 'Expected key `{}` has no value'.format(key)


class TestErratasQuery(object):
    def test_post_multi(self, rest_api):
        """Tests multiple erratas using POST."""
        request_body = tools.erratas_body(ERRATAS)
        erratas = rest_api.get_erratas(body=request_body).response_check()
        assert len(erratas) == len(ERRATAS)
        for errata_name in ERRATAS:
            assert errata_name in erratas
            check_keys(erratas[errata_name])

    @pytest.mark.parametrize('errata_name', ERRATAS)
    def test_post_single(self, rest_api, errata_name):
        """Tests single errata using POST."""
        request_body = tools.erratas_body([errata_name])
        erratas = rest_api.get_erratas(body=request_body).response_check()
        assert len(erratas) == 1
        errata, = erratas
        assert errata.name == errata_name
        check_keys(errata)

    @pytest.mark.parametrize('errata_name', ERRATAS)
    def test_get(self, rest_api, errata_name):
        """Tests single errata using GET."""
        erratas = rest_api.get_errata(errata_name).response_check()
        assert len(erratas) == 1
        errata, = erratas
        assert errata.name == errata_name
        check_keys(errata)
