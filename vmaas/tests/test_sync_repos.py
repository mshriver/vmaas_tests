# -*- coding: utf-8 -*-

from wait_for import wait_for

from vmaas.rest import exceptions


def test_repo_refresh(rest_api):
    def _refresh():
        try:
            response = rest_api.reporefresh()
        except exceptions.ClientError as err:
            if 'Another sync task already in progress' in err.response.body['msg']:
                return False
            raise
        return response

    response, __ = wait_for(_refresh, num_sec=10)
    response.response_check()
    response, = response
    assert 'Repo sync task started' in response.msg
