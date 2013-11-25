#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    ControlBeast - FreeBSD Server Management Tool Suite
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: Copyright 2013 by the ControlBeast team, see AUTHORS.
    :license: ISC, see LICENSE for details.
"""


import os
import sys


def main():
    """
    ControlBeast main function, acting as central dispatcher
    """
    # find out if running from an uninstalled version
    # this being the case, insert the appropriate path into PYTHONPATH
    cb_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    if os.path.isfile(cb_path + '/controlbeast/__init__.py'):
        sys.path.insert(0, cb_path)

    import controlbeast.cli
    return controlbeast.cli.dispatch(os.path.realpath(__file__), sys.argv)


if __name__ == '__main__':
    sys.exit(main())
else:
    raise RuntimeError("This is an executable file. Do not try to import it!")
    # noinspection PyUnreachableCode
    sys.exit(os.EX_SOFTWARE)