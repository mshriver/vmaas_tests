# -*- coding: utf-8 -*-
"""
REST API helper functions
"""

import datetime


def gen_cves_body(cves):
    """Generates request body for CVEs query out of list of CVEs."""
    return dict(cve_list=cves)


def gen_errata_body(errata):
    """Generates request body for errata query out of list of errata."""
    return dict(errata_list=errata)


def gen_repos_body(repos):
    """Generates request body for repos query out of list of repos."""
    return dict(repository_list=repos)


def gen_updates_body(packages, repositories=None, modified_since=None):
    """Generates request body for package updates query out of list of packages."""
    body = dict(package_list=packages)
    if repositories:
        body['repository_list'] = repositories
    if modified_since:
        if isinstance(modified_since, datetime.datetime):
            modified_since = modified_since.replace(microsecond=0).isoformat()
        body['modified_since'] = modified_since
    return body


def check_updates_uniq(updates):
    """Checks that returned update records are unique."""
    known_records = []
    not_unique = []
    for update in updates:
        for record in known_records:
            if record != update:
                continue
            # If we are here, the record is already known.
            # Making sure the record is added to `not_unique` list only once.
            for seen in not_unique:
                if seen == update:
                    break
            else:
                not_unique.append(record)
            break
        else:
            known_records.append(update)

    assert not not_unique, 'Duplicates found: {!r}'.format(not_unique)


def _updates_match(expected_update, available_update):
    """Checks if expected update record matches available update record."""
    for key, value in expected_update.items():
        if key not in available_update:
            return False
        # partial match for package name
        if key == 'package' and value in available_update[key]:
            continue
        # exact match for the rest of the values
        if value == available_update[key]:
            continue
        # if we are here, values don't match
        return False

    return True


def check_expected_updates(expected_updates, available_updates):
    """Checks if all expected update records are present in available updates."""
    not_found = []
    for expected_update in expected_updates:
        for available_update in available_updates:
            if _updates_match(expected_update, available_update):
                break
        else:
            not_found.append(expected_update)
    assert not not_found, 'Expected update not found: {!r}'.format(not_found)


def validate_package_updates(package, expected_updates):
    """Runs checks on response body of 'updates' query."""
    assert package.description
    assert package.summary

    # check that expected keys are available in each record
    for record in package.available_updates:
        for key in expected_updates[0]:
            assert record[key] is not None, 'Expected key `{}` has no value'.format(key)

    # check that expected updates are present in the response
    assert len(package.available_updates) >= len(expected_updates)
    check_expected_updates(expected_updates, package.available_updates)

    # check that available updates records are unique
    # disabled until GH#176 is fixed
    # check_updates_uniq(package.available_updates)
