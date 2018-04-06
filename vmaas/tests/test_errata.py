# -*- coding: utf-8 -*-

import pytest

from vmaas.rest import schemas, tools

ERRATA = [
    'RHBA-2016:2858',
    'RHSA-2017:1931',
]


class TestErrataQuery(object):
    def test_post_multi(self, rest_api):
        """Tests multiple errata using POST."""
        request_body = tools.gen_errata_body(ERRATA)
        errata = rest_api.get_errata(body=request_body).response_check()
        schemas.errata_schema.validate(errata.raw.body)
        assert len(errata) == len(ERRATA)
        for erratum_name in ERRATA:
            assert erratum_name in errata

    @pytest.mark.parametrize('erratum_name', ERRATA)
    def test_post_single(self, rest_api, erratum_name):
        """Tests single erratum using POST."""
        request_body = tools.gen_errata_body([erratum_name])
        errata = rest_api.get_errata(body=request_body).response_check()
        schemas.errata_schema.validate(errata.raw.body)
        assert len(errata) == 1
        erratum, = errata
        assert erratum.name == erratum_name

    @pytest.mark.parametrize('erratum_name', ERRATA)
    def test_get(self, rest_api, erratum_name):
        """Tests single erratum using GET."""
        errata = rest_api.get_erratum(erratum_name).response_check()
        schemas.errata_schema.validate(errata.raw.body)
        assert len(errata) == 1
        erratum, = errata
        assert erratum.name == erratum_name
