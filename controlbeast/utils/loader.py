# -*- coding: utf-8 -*-
"""
    controlbeast.utils.loader
    ~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: Copyright 2013 by the ControlBeast team, see AUTHORS.
    :license: ISC, see LICENSE for details.
"""

import importlib
import os
import re


def __filter_members(item):
    """
    Filter function to detect classes within a module or package

    :param item: the item to be tested with this filter
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


def __filter_modules(item):
    """
    Filter function to detect processor modules and packages

    :param item: the item to be tested with this filter
    """
    exclude = (
        re.escape('__init__.py'),
        re.escape('base.py')
    )
    pattern = re.compile('|'.join(exclude))
    return not pattern.search(item)


def detect_class_modules(module, parent=object):
    """
    Detect available class modules or packages and return a dictionary of valid class names, referring to
    the module they are contained within.

    :param module: the module or package to be scanned for classes
    :param parent: the class potential candidates must be derived off
    """

    # initialise result dictionary
    result = {}

    # get a list of all files and directories inside the module
    try:
        package_instance = importlib.import_module(module)
    except ImportError:
        return result

    if package_instance.__file__[-11:] == '__init__.py':
        gen_dir = os.listdir(os.path.dirname(os.path.realpath(package_instance.__file__)))
    else:
        gen_dir = [os.path.realpath(package_instance.__file__)]

    # only consider modules and packages, and exclude the base module
    for file_candidate in filter(__filter_modules, gen_dir):

        # Python files are modules; the name needs to be without file ending
        if file_candidate[-3:] == '.py':
            file_candidate = file_candidate[:-3]

        # try if the detected package or module can be imported
        try:
            class_module_candidate = importlib.import_module('.'.join([module, file_candidate]))
        except ImportError:
            class_module_candidate = None

        # if the module or module could be imported, test if it contains classes derived from the parent class
        if class_module_candidate:
            for member_candidate in filter(__filter_members, dir(class_module_candidate)):
                try:
                    if issubclass(getattr(class_module_candidate, member_candidate), parent) \
                       and getattr(class_module_candidate, member_candidate).__name__ != parent.__name__:
                        result[member_candidate] = class_module_candidate.__name__
                except TypeError:
                    pass

    # return the dictionary
    return result


def load_member(module, member):
    """
    Load a member (function, class, ...) from a module and return it

    :param module: the module or package name where the class should be loaded from
    :param member: the name of the member to be loaded
    """
    try:
        module = importlib.import_module(module)
    except ImportError:
        return None
    try:
        result = getattr(module, member)
    except AttributeError:
        return None
    return result