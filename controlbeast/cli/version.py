# -*- coding: utf-8 -*-
"""
    controlbeast.cli.version
    ~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: Copyright 2013 by the ControlBeast team, see AUTHORS.
    :license: ISC, see LICENSE for details.
"""

import controlbeast
import controlbeast.cli.base


class VersionCommand(controlbeast.cli.base.CbCommand):
    """
    Command class implementing the version command
    """
    _help = 'Show version and copyright information'
    _arg_list = (
        (('-s', '--short'), {'help': 'only print the version string', 'action': 'store_true'}),
    )

    def handle(self):
        """
        Command handler for the version command
        """
        if 'short' in self._args and self._args.short:
            print(controlbeast.get_version())
        else:
            print("""ControlBeast version {version}

Copyright (C) {year} by {author}
This is free software; see the source for copying conditions. There is NO
warranty; not even for MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. """.format(
                version=controlbeast.get_version(),
                year=controlbeast.COPYRIGHT[0],
                author=controlbeast.COPYRIGHT[1])
            )
        self._status = 0