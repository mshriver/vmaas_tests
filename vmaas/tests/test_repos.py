# -*- coding: utf-8 -*-

import pytest

from vmaas.rest import tools

REPOS = [
    ('rhel-7-server-rpms', 1),
    ('rhel-6-workstation-rpms', 1),
]

EXPECTED_KEYS = [
    'product',
    'releasever',
    'name',
    'url',
    'basearch',
    'label',
]


def check_keys(repo_records):
    for record in repo_records:
        for key in EXPECTED_KEYS:
            assert record[key] is not None, 'Expected key `{}` has no value'.format(key)


class TestReposQuery(object):
    def test_post_multi(self, rest_api):
        """Tests multiple repos using POST."""
        request_body = tools.gen_repos_body([p[0] for p in REPOS])
        repos = rest_api.get_repos(body=request_body).response_check()
        assert len(repos) == len(REPOS)
        for repo_name, min_expected in REPOS:
            assert len(repos[repo_name]) >= min_expected
            check_keys(repos[repo_name])

    @pytest.mark.parametrize('repo', REPOS, ids=[p[0] for p in REPOS])
    def test_post_single(self, rest_api, repo):
        """Tests single repo using POST."""
        repo_name, min_expected = repo
        request_body = tools.gen_repos_body([repo_name])
        repos = rest_api.get_repos(body=request_body).response_check()
        assert len(repos) == 1
        repo, = repos
        assert len(repo) >= min_expected
        check_keys(repo)

    @pytest.mark.parametrize('repo', REPOS, ids=[p[0] for p in REPOS])
    def test_get(self, rest_api, repo):
        """Tests single repo using GET."""
        repo_name, min_expected = repo
        repos = rest_api.get_repo(repo_name).response_check()
        assert len(repos) == 1
        repo, = repos
        assert len(repo) >= min_expected
        check_keys(repo)
