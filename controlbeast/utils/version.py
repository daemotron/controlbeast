# -*- coding: utf-8 -*-
"""
    controlbeast.utils.version
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: Copyright 2013 by the ControlBeast team, see AUTHORS.
    :license: ISC, see LICENSE for details.
"""
from controlbeast.utils.convert import to_str
import controlbeast
import os.path
import subprocess
import datetime


def get_version(*args, **kwargs):
    """Derives a PEP386-compliant version number from VERSION."""
    if 'version' in kwargs:
        version = kwargs['version']
    elif args:
        version = args[0]
    else:
        from controlbeast import VERSION

        version = VERSION

    assert len(version) == 5
    assert version[3] in ('alpha', 'beta', 'rc', 'final')

    # Now build the two parts of the version number:
    # main = X.Y[.Z]
    # sub = .devN - for pre-alpha releases
    #     | {a|b|c}N - for alpha, beta and rc releases

    parts = 2 if version[2] == 0 else 3
    main = '.'.join(str(x) for x in version[:parts])

    sub = ''
    if version[3] == 'alpha' and version[4] == 0:
        git_revision = get_git_changeset()[4:]
        if git_revision != 'unknown':
            sub = '.dev{revision}'.format(revision=git_revision)
        else:
            sub = '.dev'

    elif version[3] != 'final':
        mapping = {'alpha': 'a', 'beta': 'b', 'rc': 'c'}
        sub = mapping[version[3]] + str(version[4])

    return main + sub


def get_git_revision(path=None):
    """
    Returns the Git revision (short) in the form GIT-xxxxxxx,
    where xxxxxxx is the (short) Git revision hash.

    Returns GIT-unknown if anything goes wrong, such as unexpected
    format of internal Git files.

    If path is provided, it should be a directory being a valid Git
    repository (non-bare). If it is not provided, this function will
    use the root controlbeast/ package directory.
    """

    rev = None
    if path is None:
        path = controlbeast.__path__[0]

    head_path = os.path.normpath(os.path.join(path, '../.git/HEAD'))

    try:
        head = open(head_path, 'r').read()
    except IOError:
        pass
    else:
        ref_path = os.path.join(path, '../.git', head.split(':')[1].strip())
        ref_path = os.path.normpath(ref_path)
        try:
            ref = open(ref_path, 'r').read()
        except IOError:
            pass
        else:
            rev = ref[:7]

    if rev:
        return 'GIT-{revision}'.format(revision=rev)
    return 'GIT-unknown'


def get_git_changeset(path=None):
    """
    Returns a numeric identifier of the latest Git changeset.

    Since the Git revision hash does not fulfil the requirements
    of PEP 386, the UTC timestamp in YYYYMMDDHHMMSS format is used
    instead. This value is not guaranteed to be unique, however the
    likeliness of collisions is small enough to be acceptable for
    the purpose of building version numbers.
    """
    if path is None:
        path = os.path.normpath(os.path.join(controlbeast.__path__[0], ".."))

    # run `git show` in ControlBeast's root directory and grab its output from stdout
    try:
        with subprocess.Popen(
            'git show --pretty=format:%ct --quiet HEAD',
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True,
            cwd=path,
            universal_newlines=True
        ) as git_show:
            timestamp = to_str(git_show.communicate()[0]).partition('\n')[0]
    except OSError:
        timestamp = None

    try:
        timestamp = datetime.datetime.utcfromtimestamp(int(timestamp))
    except (ValueError, TypeError):
        return 'GIT-unknown'

    return 'GIT-{0:>s}'.format(timestamp.strftime('%Y%m%d%H%M%S'))
