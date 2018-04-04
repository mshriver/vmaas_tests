# -*- coding: utf-8 -*-

import pytest

from vmaas.rest import tools


EXPECTED_BASH = [
    {
        "erratum": "RHSA-2017:1931",
        "repository": "rhel-7-server-rpms",
        "package": "bash-"
    },
    {
        "erratum": "RHSA-2017:1931",
        "repository": "rhel-7-workstation-rpms",
        "package": "bash-"
    },
]

EXPECTED_BASH_W_REPO = [
    {
        "erratum": "RHSA-2017:1931",
        "repository": "rhel-7-server-rpms",
        "package": "bash-"
    },
]

EXPECTED_POSTGRES = [
    {
        "erratum": "RHSA-2017:3402",
        "repository": "rhel-7-server-rpms",
        "package": "postgresql-"
    },
    {
        "erratum": "RHSA-2017:3402",
        "repository": "rhel-7-workstation-rpms",
        "package": "postgresql-"
    },
    {
        "erratum": "RHSA-2017:2728",
        "repository": "rhel-7-server-rpms",
        "package": "postgresql-"
    },
    {
        "erratum": "RHSA-2017:2728",
        "repository": "rhel-7-workstation-rpms",
        "package": "postgresql-"
    },
    {
        "erratum": "RHSA-2017:1983",
        "repository": "rhel-7-server-rpms",
        "package": "postgresql-"
    },
    {
        "erratum": "RHSA-2017:1983",
        "repository": "rhel-7-workstation-rpms",
        "package": "postgresql-"
    },
]

EXPECTED_POSTGRES_W_REPO = [
    {
        "erratum": "RHSA-2017:3402",
        "repository": "rhel-7-server-rpms",
        "package": "postgresql-"
    },
    {
        "erratum": "RHSA-2017:2728",
        "repository": "rhel-7-server-rpms",
        "package": "postgresql-"
    },
    {
        "erratum": "RHSA-2017:1983",
        "repository": "rhel-7-server-rpms",
        "package": "postgresql-"
    },
]

EXPECTED_POSTGRES_DEVEL = [
    {
        "erratum": "RHSA-2017:1983",
        "repository": "rhel-7-server-rpms",
        "package": "postgresql-devel-"
    },
    {
        "erratum": "RHSA-2017:1983",
        "repository": "rhel-7-workstation-rpms",
        "package": "postgresql-devel-"
    },
    {
        "erratum": "RHSA-2017:2728",
        "repository": "rhel-7-server-rpms",
        "package": "postgresql-devel-"
    },
    {
        "erratum": "RHSA-2017:2728",
        "repository": "rhel-7-workstation-rpms",
        "package": "postgresql-devel-"
    },
    {
        "erratum": "RHSA-2017:3402",
        "repository": "rhel-7-server-rpms",
        "package": "postgresql-devel-"
    },
    {
        "erratum": "RHSA-2017:3402",
        "repository": "rhel-7-workstation-rpms",
        "package": "postgresql-devel-"
    }
]

EXPECTED_POSTGRES_DEVEL_W_REPO = [
    {
        "erratum": "RHSA-2017:1983",
        "repository": "rhel-7-server-rpms",
        "package": "postgresql-devel-"
    },
    {
        "erratum": "RHSA-2017:2728",
        "repository": "rhel-7-server-rpms",
        "package": "postgresql-devel-"
    },
    {
        "erratum": "RHSA-2017:3402",
        "repository": "rhel-7-server-rpms",
        "package": "postgresql-devel-"
    },
]

PACKAGES = [
    # package, expected updates
    ('bash-0:4.2.46-20.el7_2.x86_64', EXPECTED_BASH),
    ('postgresql-0:9.2.18-1.el7.x86_64', EXPECTED_POSTGRES),
    ('postgresql-devel-9.2.18-1.el7.x86_64', EXPECTED_POSTGRES_DEVEL),
]

PACKAGES_W_REPOS = [
    # package, expected updates
    ('bash-0:4.2.46-20.el7_2.x86_64', EXPECTED_BASH_W_REPO),
    ('postgresql-0:9.2.18-1.el7.x86_64', EXPECTED_POSTGRES_W_REPO),
    ('postgresql-devel-9.2.18-1.el7.x86_64', EXPECTED_POSTGRES_DEVEL_W_REPO),
]

REPOS = [
    'rhel-6-workstation-rpms',
    'rhel-7-server-rpms',
]


class TestUpdatesAll(object):
    def test_post_multi(self, rest_api):
        """Tests updates using POST with multiple packages."""
        request_body = tools.gen_updates_body([p[0] for p in PACKAGES])
        updates = rest_api.get_updates(body=request_body).response_check()
        assert len(updates) == len(PACKAGES)
        for package_name, expected_updates in PACKAGES:
            package = updates[package_name]
            tools.validate_package_updates(package, expected_updates)

    @pytest.mark.parametrize('package_record', PACKAGES, ids=[p[0] for p in PACKAGES])
    def test_post_single(self, rest_api, package_record):
        """Tests updates using POST with single package."""
        name, expected_updates = package_record
        request_body = tools.gen_updates_body([name])
        updates = rest_api.get_updates(body=request_body).response_check()
        assert len(updates) == 1
        package, = updates
        tools.validate_package_updates(package, expected_updates)

    @pytest.mark.parametrize('package_record', PACKAGES, ids=[p[0] for p in PACKAGES])
    def test_get(self, rest_api, package_record):
        """Tests updates using GET with single package."""
        name, expected_updates = package_record
        updates = rest_api.get_update(name).response_check()
        assert len(updates) == 1
        package, = updates
        tools.validate_package_updates(package, expected_updates)


class TestUpdatesInRepos(object):
    def test_post_multi(self, rest_api):
        """Tests updates in repos using POST with multiple packages."""
        request_body = tools.gen_updates_body([p[0] for p in PACKAGES_W_REPOS], repositories=REPOS)
        updates = rest_api.get_updates(body=request_body).response_check()
        assert len(updates) == len(PACKAGES_W_REPOS)
        for package_name, expected_updates in PACKAGES_W_REPOS:
            package = updates[package_name]
            tools.validate_package_updates(package, expected_updates)

    @pytest.mark.parametrize(
        'package_record', PACKAGES_W_REPOS, ids=[p[0] for p in PACKAGES_W_REPOS])
    def test_post_single(self, rest_api, package_record):
        """Tests updates in repos using POST with single package."""
        name, expected_updates = package_record
        request_body = tools.gen_updates_body([name], repositories=REPOS)
        updates = rest_api.get_updates(body=request_body).response_check()
        assert len(updates) == 1
        package, = updates
        tools.validate_package_updates(package, expected_updates)
