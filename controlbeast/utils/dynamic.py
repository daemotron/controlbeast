# -*- coding: utf-8 -*-
"""
    controlbeast.utils.dynamic
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: Copyright 2013 by the ControlBeast team, see AUTHORS.
    :license: ISC, see LICENSE for details.
"""


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