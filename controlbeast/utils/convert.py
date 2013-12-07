# -*- coding: utf-8 -*-
"""
    controlbeast.utils.convert
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: Copyright 2013 by the ControlBeast team, see AUTHORS.
    :license: ISC, see LICENSE for details.
"""


def to_bytes(value):
    """
    Convert any value into a byte sequence.

    :param value: The value to be converted
    :return: Byte sequence
    """
    if isinstance(value, str):
        return bytes(value, 'utf-8', 'replace')
    elif isinstance(value, bytearray):
        return bytes(value)
    elif isinstance(value, bytes):
        return value
    elif value is None:
        return b''
    else:
        return bytes(str(value), 'utf-8', 'replace')


def to_str(value):
    """
    Convert any value into a string.

    :param value: The value to be converted
    :return: Resulting string
    """
    if isinstance(value, bytes) or isinstance(value, bytearray):
        return value.decode('utf-8', 'replace')
    elif value is None:
        return ''
    else:
        return str(value)