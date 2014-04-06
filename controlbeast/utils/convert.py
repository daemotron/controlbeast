# -*- coding: utf-8 -*-
"""
    controlbeast.utils.convert
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: Copyright 2013 by the ControlBeast team, see AUTHORS.
    :license: ISC, see LICENSE for details.
"""
from controlbeast.conf import get_conf


def to_bytes(value):
    """
    Convert any value into a byte sequence.

    :param value: The value to be converted
    :return: Byte sequence
    """
    if isinstance(value, str):
        # noinspection PyArgumentList
        return bytes(source=value, encoding=get_conf('DEFAULT_CHARSET'), errors='replace')
    elif isinstance(value, bytearray):
        return bytes(value)
    elif isinstance(value, bytes):
        return value
    elif not value:
        return b''
    else:
        # noinspection PyArgumentList
        return bytes(source=str(value), encoding=get_conf('DEFAULT_CHARSET'), errors='replace')


def to_str(value):
    """
    Convert any value into a string.

    :param value: The value to be converted
    :return: Resulting string
    """
    if isinstance(value, bytes) or isinstance(value, bytearray):
        return value.decode(encoding=get_conf('DEFAULT_CHARSET'), errors='replace')
    elif value is None:
        return ''
    else:
        return str(value)
