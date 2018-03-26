# -*- coding: utf-8 -*-

import pytest

from utils.rest import tools

PACKAGES = [
    # package, minimal number of expected errata
    ('bash-0:4.2.46-20.el7_2.x86_64', 4),
    ('postgresql-0:9.2.18-1.el7.x86_64', 12),
    ('postgresql-devel-9.2.18-1.el7.x86_64', 12),
]

PACKAGES_W_REPOS = [
    # package, minimal number of expected errata
    ('bash-0:4.2.46-20.el7_2.x86_64', 2),
    ('postgresql-0:9.2.18-1.el7.x86_64', 6),
    ('postgresql-devel-9.2.18-1.el7.x86_64', 6),
]

REPOS = [
    'rhel-6-workstation-rpms',
    'rhel-7-server-rpms',
]


EXPECTED_KEYS = [
    'erratum',
    'repository',
    'package',
]


def check_keys(package_records):
    for record in package_records:
        for key in EXPECTED_KEYS:
            assert record[key] is not None, 'Expected key `{}` has no value'.format(key)


class TestUpdatesAll(object):
    def test_post_multi(self, rest_api):
        """Tests updates using POST with multiple packages."""
        request_body = tools.updates_body([p[0] for p in PACKAGES])
        updates = rest_api.get_updates(body=request_body).response_check()
        assert len(updates) == len(PACKAGES)
        for package, min_expected in PACKAGES:
            assert len(updates[package]) >= min_expected
            check_keys(updates[package])

    @pytest.mark.parametrize('package', PACKAGES, ids=[p[0] for p in PACKAGES])
    def test_post_single(self, rest_api, package):
        """Tests updates using POST with single package."""
        name, min_expected = package
        request_body = tools.updates_body([name])
        updates = rest_api.get_updates(body=request_body).response_check()
        assert len(updates) == 1
        update, = updates
        assert len(update) >= min_expected
        check_keys(update)

    @pytest.mark.parametrize('package', PACKAGES, ids=[p[0] for p in PACKAGES])
    def test_get(self, rest_api, package):
        """Tests updates using GET with single package."""
        name, min_expected = package
        updates = rest_api.get_update(name).response_check()
        assert len(updates) == 1
        update, = updates
        assert len(update) >= min_expected
        check_keys(update)


class TestUpdatesInRepos(object):
    def test_post_multi(self, rest_api):
        """Tests updates in repos using POST with multiple packages."""
        request_body = tools.updates_body([p[0] for p in PACKAGES_W_REPOS], repositories=REPOS)
        updates = rest_api.get_updates(body=request_body).response_check()
        assert len(updates) == len(PACKAGES_W_REPOS)
        for package, min_expected in PACKAGES_W_REPOS:
            assert len(updates[package]) >= min_expected
            check_keys(updates[package])

    @pytest.mark.parametrize('package', PACKAGES_W_REPOS, ids=[p[0] for p in PACKAGES_W_REPOS])
    def test_post_single(self, rest_api, package):
        """Tests updates in repos using POST with single package."""
        name, min_expected = package
        request_body = tools.updates_body([name], repositories=REPOS)
        updates = rest_api.get_updates(body=request_body).response_check()
        assert len(updates) == 1
        update, = updates
        assert len(update) >= min_expected
        check_keys(update)
