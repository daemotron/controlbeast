# -*- coding: utf-8 -*-
"""
    controlbeast.utils.singleton
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: Copyright 2013 by the ControlBeast team, see AUTHORS.
    :license: ISC, see LICENSE for details.
"""


class CbSingleton:
    """
    Auxiliary class to ease implementing lazy singletons.
    This class must be applied as a decorator instead of inheriting from this class.

    The decorated class can define one `__init__` function, but this constructor is restricted to the `self` argument.

    To get the singleton instance, use the `get_instance` method. Trying to use `__call__` will result in a
    `TypeError` being raised. The actual instance will not be created before `get_instance` has been called
    (lazy behaviour).

    Other limitations: The decorated class cannot be inherited from.
    """

    def __init__(self, decorated):
        self._decorated = decorated

    def get_instance(self):
        """
        Returns the singleton instance. Upon its first call, it creates a
        new instance of the decorated class and calls its `__init__` method.
        On all subsequent calls, the already created instance is returned.
        """
        try:
            return self._instance
        except AttributeError:
            self._instance = self._decorated()
            return self._instance

    def __call__(self):
        raise TypeError('Singletons must be accessed through `get_instance()`.')

    def __instancecheck__(self, inst):
        return isinstance(inst, self._decorated)