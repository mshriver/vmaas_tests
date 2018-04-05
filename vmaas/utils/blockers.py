# -*- coding: utf-8 -*-
"""
Blockers using GitHub issues.
"""

# Implementation copied from ManageIQ/integration_tests

import logging
import re

from github import Github

from vmaas.utils.conf import conf

logger = logging.getLogger(__name__)


class _classproperty(property):
    """Subclass property to make classmethod properties possible."""
    def __get__(self, cls, owner):
        # pylint: disable=no-member
        return self.fget.__get__(None, owner)()


def classproperty(func):
    """Enables properties for whole classes:

    Usage:

        >>> class Foo(object):
        ...     @classproperty
        ...     def bar(cls):
        ...         return "bar"
        ...
        >>> print(Foo.bar)
        baz
    """
    return _classproperty(classmethod(func))


class Blocker(object):
    """Base class for all blockers.

    REQUIRED THING! Any subclass' constructors must accept kwargs and after POPping the values
    required for the blocker's operation, `call to ``super`` with ``**kwargs`` must be done!
    Failing to do this will render some of the functionality disabled ;)
    """
    blocks = False
    kwargs = {}

    def __init__(self, **kwargs):
        self.forced_streams = kwargs.pop('forced_streams', [])
        self.__dict__['kwargs'] = kwargs

    @property
    def url(self):
        raise NotImplementedError('You need to implement .url')

    @classmethod
    def all_blocker_engines(cls):
        """Return mapping of name:class of all the blocker engines in this module.

        Having this as a separate function will later enable to scatter the engines across modules
        in case of extraction into a separate library.
        """
        return {
            'GH': GH,
        }

    @classmethod
    def parse(cls, blocker, **kwargs):
        """Create a blocker object from some representation."""
        if isinstance(blocker, cls):
            return blocker
        elif isinstance(blocker, str):
            if "#" in blocker:
                # Generic blocker
                engine, spec = blocker.split('#', 1)
                try:
                    engine_class = cls.all_blocker_engines()[engine]
                except KeyError:
                    raise ValueError(
                        '{} is a wrong engine specification for blocker! ({} available)'.format(
                            engine, ", ".join(cls.all_blocker_engines().keys())))
                return engine_class(spec, **kwargs)
            raise ValueError('Could not parse blocker {}'.format(blocker))
        else:
            raise ValueError('Wrong specification of the blockers!')


class GH(Blocker):
    """GitHub issues blocker."""
    DEFAULT_REPOSITORY = conf.get('github', {}).get('upstream_repo')
    _issue_cache = {}

    @classproperty
    # pylint: disable=no-self-argument,attribute-defined-outside-init
    def github(cls):
        if not hasattr(cls, '_github'):
            token = conf.get('github', {}).get('token')
            if token is not None:
                cls._github = Github(token)
            else:
                cls._github = Github()  # Without auth max 60 req/hr
        return cls._github

    def __init__(self, description, **kwargs):
        super(GH, self).__init__(**kwargs)
        self._repo = None
        self.issue = None
        if isinstance(description, (list, tuple)):
            try:
                self.repo, self.issue = description
                self.issue = int(self.issue)
            except ValueError:
                raise ValueError(
                    'The GH issue specification must have 2 items and issue must be number')
        elif isinstance(description, int):
            if self.DEFAULT_REPOSITORY is None:
                raise ValueError('You must specify github/upstream_repo in env.yaml!')
            self.issue = description
        elif isinstance(description, str):
            try:
                owner, repo, issue_num = re.match(r'^([^/]+)/([^/:]+):([0-9]+)$',
                                                  str(description).strip()).groups()
            except AttributeError:
                raise ValueError(
                    'Could not parse `{!s}` as a proper GH issue anchor!'.format(description))
            else:
                self._repo = '{}/{}'.format(owner, repo)
                self.issue = int(issue_num)
        else:
            raise ValueError('GH issue specified wrong')

    @property
    def data(self):
        identifier = "{}:{}".format(self.repo, self.issue)
        if identifier not in self._issue_cache:
            # pylint: disable=no-member
            self._issue_cache[identifier] = self.github.get_repo(self.repo).get_issue(self.issue)
        return self._issue_cache[identifier]

    @property
    def blocks(self):
        if self.data.state == 'closed':
            return False
        return True

    @property
    def repo(self):
        return self._repo or self.DEFAULT_REPOSITORY

    def __str__(self):
        return 'GitHub Issue https://github.com/{}/issues/{}'.format(self.repo, self.issue)

    @property
    def url(self):
        return 'https://github.com/{}/issues/{}'.format(self.repo, self.issue)
