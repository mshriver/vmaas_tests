# -*- coding: utf-8 -*-

import pytest


@pytest.mark.skip(reason='GH#166')
def test_repo_refresh(rest_api):
    response = rest_api.reporefresh().response_check()
    response, = response
    assert 'Repo sync task started' in response.msg
