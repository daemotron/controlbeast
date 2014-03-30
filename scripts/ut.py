#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    ControlBeast - FreeBSD Server Management Tool Suite Test Script
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: Copyright 2013, 2014 by the ControlBeast team, see AUTHORS.
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
        module_prefix = '.'.join(str(os.path.relpath(root, os.path.dirname(test_dir))).split(os.path.sep))
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

    results = {}
    skipped = []

    # Create a unittest runner and run all detected tests
    runner = unittest.TextTestRunner(stream=open('/dev/null', 'w'))
    for test_class in test_classes:
        suite = unittest.defaultTestLoader.loadTestsFromTestCase(test_class)
        result = runner.run(suite)
        if result.skipped:
            for test in result.skipped:
                skipped.append((test_class.__name__, test[0], test[1]))
        results[test_class.__name__] = (len(result.failures), len(result.skipped), result.testsRun)
        if result.failures:
            return_code = os.EX_SOFTWARE

    total_tests = 0
    total_passed = 0
    total_failed = 0
    total_skipped = 0

    print("\nControlBeast Unit Test Result Summary:\n")
    print("Test                   Passed   Failed   Skipped   Total    % passed")
    print("====================================================================")
    for key in sorted(results):
        total_tests += results[key][2]
        total_skipped += results[key][1]
        total_failed += results[key][0]
        total_passed = total_tests - total_failed - total_skipped
        print(
            "{test: <20}      {passed: >3d}      {failed: >3d}      {skipped: >4d}     {total: >3d}     {ratio: >3.2%}".format(
            test=key,
            passed=results[key][2]-results[key][0]-results[key][1],
            failed=results[key][0],
            skipped=results[key][1],
            total=results[key][2],
            ratio=(results[key][2]-results[key][0]-results[key][1])/(results[key][2]-results[key][1])
        ))
    print("====================================================================")
    print("{test: <20}      {passed: >3d}      {failed: >3d}      {skipped: >4d}     {total: >3d}     {ratio: >3.2%}\n".format(
        test="TOTAL",
        passed=total_passed,
        failed=total_failed,
        skipped=total_skipped,
        total=total_tests,
        ratio=total_passed/(total_tests-total_skipped)
    ))
    if skipped:
        print('Skipped Test Cases:\n')
        for skip in skipped:
            print('   {module} {test}: {reason}'.format(
                module=skip[0],
                test=' '.join(str(skip[1]).split(" ")[0].split('_')),
                reason=skip[2].strip())
            )

    if total_passed < (total_tests - total_skipped):
        print("\nOverall Test Result: FAILED.\n")
    else:
        print("\nOverall Test Result: PASSED.\n")
    return return_code


if __name__ == '__main__':
    sys.exit(main())
else:
    raise RuntimeError("This is an executable file. Do not try to import it!")
    # noinspection PyUnreachableCode
    sys.exit(os.EX_SOFTWARE)
