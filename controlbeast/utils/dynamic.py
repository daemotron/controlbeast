# -*- coding: utf-8 -*-
"""
    controlbeast.utils.dynamic
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: Copyright 2013 by the ControlBeast team, see AUTHORS.
    :license: ISC, see LICENSE for details.
"""
from collections import UserDict


class CbDynamic(object):
    """
    Dynamic class generating properties from kwargs
    """

    def __init__(self, *args, **kwargs):
        """
        Construct properties from keyword arguments
        """
        for elem in kwargs:
            self.__add_property(elem, kwargs[elem])

    def __add_property(self, name, value, doc=None):
        """
        Dynamically add property (read-only) to the current class object
        """
        fget = lambda self: self._get_property(name)
        setattr(self.__class__, name, property(fget, doc=doc))
        setattr(self, '_' + name, value)

    def _get_property(self, name):
        """
        Get property by its internal name
        """
        return getattr(self, '_' + name)


class CbDynamicIterable(UserDict):
    """
    A dynamic iterable object is similar to a normal Python dictionary, except it offers
    all keys also as properties.

    :param dict dict: dictionary with initial data to be filled in
    :param kwargs:    keyword arguments to be transformed into dictionary data
    """

    def __init__(self, dict=None, **kwargs):
        super(CbDynamicIterable, self).__init__(dict=dict, **kwargs)

    def __add_property(self, name, value, doc=None):
        """
        Dynamically add property to the current class object
        """
        fget = lambda self: self[name]
        fset = lambda self, value: self.__setitem__(name, value)
        setattr(self.__class__, name, property(fget=fget, fset=fset, doc=doc))

    def __del_property(self, name):
        """
        Dynamically delete property and internal representation
        """
        delattr(self.__class__, name)

    def __setitem__(self, key, item):
        """
        Overrides default ``__setitem__`` method. Functionality is identical, except a property with
        the key name is created or updated.
        """
        self.__add_property(key, item)
        super(CbDynamicIterable, self).__setitem__(key, item)

    def __delitem__(self, key):
        """
        Overrides default ``__delitem__`` method. Functionality is identical, the property with
        the key name is deleted.
        """
        self.__del_property(key)
        super(CbDynamicIterable, self).__delitem__(key)
