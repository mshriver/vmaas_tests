# -*- coding: utf-8 -*-

import pytest


@pytest.mark.skip(reason='GH#166')
def test_sync_cves(rest_api):
    response = rest_api.cvescan().response_check()
    response, = response
    assert 'CVE sync task started' in response.msg
