#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    ControlBeast - FreeBSD Server Management Tool Suite Test Script
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: Copyright 2013 by the ControlBeast team, see AUTHORS.
    :license: ISC, see LICENSE for details.
"""
import importlib

import os
import re
import sys
import unittest


def __filter_files(item):
    """
    Filter for Python modules beginning with *test_*

    :param str item: the item to be tested with this filter
    """
    file, ext = os.path.splitext(item)
    if file != '__init__' and ext == '.py' and file[:5] == 'test_':
        return True
    return False


def __filter_members(item):
    """
    Filter function to detect classes within a module or package

    :param str item: the item to be tested with this filter
    """
    exclude = (
        re.escape('__builtins__'),
        re.escape('__cached__'),
        re.escape('__doc__'),
        re.escape('__file__'),
        re.escape('__loader__'),
        re.escape('__name__'),
        re.escape('__package__'),
        re.escape('__path__')
    )
    pattern = re.compile('|'.join(exclude))
    return not pattern.search(item)


def main():
    """
    ControlBeast test script main function
    """
    # find out if running from an uninstalled version
    # this being the case, insert the appropriate path into PYTHONPATH
    cb_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    if os.path.isfile(cb_path + '/controlbeast/__init__.py'):
        sys.path.insert(0, cb_path)

    test_classes = []
    test_dir = os.path.join(cb_path, 'test')

    # look recursively for Python modules in ``test_dir`` and find all classes within those
    # modules derived from :py:class:`~unittest.TestCase`
    for root, dirs, files in os.walk(test_dir):
        module_prefix = '.'.join(os.path.relpath(root, os.path.dirname(test_dir)).split('/'))
        for module in filter(__filter_files, files):
            try:
                candidate = importlib.import_module('.'.join((module_prefix, os.path.splitext(module)[0])))
            except ImportError:
                candidate = None
            if candidate:
                for member in filter(__filter_members, dir(candidate)):
                    try:
                        if issubclass(getattr(candidate, member), unittest.TestCase) \
                           and getattr(candidate, member).__name__ != unittest.TestCase.__name__:
                            test_classes.append(getattr(candidate, member))
                    except TypeError:
                        pass

    return_code = os.EX_OK

    # Create a unittest runner and run all detected tests
    runner = unittest.TextTestRunner()
    for test_class in test_classes:
        suite = unittest.defaultTestLoader.loadTestsFromTestCase(test_class)
        result = runner.run(suite)
        if result.failures:
            return_code = os.EX_SOFTWARE

    return return_code


if __name__ == '__main__':
    sys.exit(main())
else:
    raise RuntimeError("This is an executable file. Do not try to import it!")
    # noinspection PyUnreachableCode
    sys.exit(os.EX_SOFTWARE)
