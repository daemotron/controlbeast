# -*- coding: utf-8 -*-
"""
    controlbeast.conf
    ~~~~~~~~~~~~~~~~~

    :copyright: Copyright 2014 by the ControlBeast team, see AUTHORS.
    :license: ISC, see LICENSE for details.
"""

from controlbeast.conf import default
from controlbeast.utils.dynamic import CbDynamicIterable
from controlbeast.utils.singleton import CbSingleton


def get_conf(key):
    """
    Get a global configuration value by its key.

    :param str key: string identifying the requested configuration value
    :returns the requested configuration value or None
    """
    configuration = CbConf.get_instance()
    if key.upper() in configuration:
        return configuration[key.upper()]
    else:
        return None


@CbSingleton
class CbConf(CbDynamicIterable):
    """
    Global ControlBeast configuration object.

    This class acts as a proxy to all configuration information set in
    :py:mod:`~controlbeast.conf.default`. The configuration data can be
    accessed either as :py:func:`property` of the :py:class:`~controlbeast.conf.CbConf`
    object, or as *(key, value)* pair via the :py:class:`~controlbeast.conf.CbConf`
    dictionary interface.

    .. note::

       Only uppercase configuration values are taken into account.

    This class is implemented following the singleton pattern. Therefore,
    in order to getting a reference to the library, the
    :py:meth:`~controlbeast.utils.singleton.CbSingleton.get_instance` method has to be used.

    Example::

       configuration = CbConf.get_instance()
    """

    def __init__(self):

        # ensure the constructor of the CbDynamicIterable parent side is called
        super(CbDynamicIterable, self).__init__(dict=None)

        # convert all upper case configuration values from :py:module:`~controlbeast.conf.default`
        for setting in dir(default):
            if setting.isupper():
                self[setting] = getattr(default, setting)
