#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    ControlBeast Setup
    ~~~~~~~~~~~~~~~~~~

    :copyright: Copyright 2014 by the ControlBeast team, see AUTHORS.
    :license: ISC, see LICENSE for details.
"""
import os
from distutils.core import setup


def get_packages(path='controlbeast'):
    """
    Recursively scan the indicated root directory for packages to be installed.

    :param str path: directory relative to this script's path
    :return: list of package names
    """
    result = []
    start = os.path.join(os.path.dirname(os.path.realpath(__file__)), path)
    for root, dirs, files in os.walk(start):
        package_candidate = '.'.join(str(os.path.relpath(root, os.path.dirname(start))).split(os.path.sep))
        if '__init__.py' in files:
            result.append(package_candidate)
    return result


def get_long_description(file='README.rst'):
    """
    Read the content of the indicated file and return it.

    :param str file: file to read the content from
    :return: a string as read from the file
    """
    desc = ''
    with open(file) as fp:
        desc = fp.read()
    return desc


setup(
    name='controlbeast',
    version=__import__('controlbeast').get_version(),
    url='https://github.com/daemotron/controlbeast',
    license='ISC License',
    author='The ControlBeast Team',
    author_email='team@controlbeast.org',
    description='Command line utility for managing configuration and automatizing maintenance of FreeBSD systems.',
    long_description=get_long_description(),
    packages=get_packages(),
    scripts=['scripts/cb.py'],
    classifiers=[
        __import__('controlbeast').get_development_status(),
        'Environment :: Console',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: ISC License (ISCL)',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: System :: Installation/Setup',
        'Topic :: System :: Software Distribution',
        'Topic :: System :: Systems Administration',
        'Topic :: Utilities'
    ]
)
