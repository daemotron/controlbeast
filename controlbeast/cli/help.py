# -*- coding: utf-8 -*-
"""
    controlbeast.cli.help
    ~~~~~~~~~~~~~~~~~~~~~

    :copyright: Copyright 2013 by the ControlBeast team, see AUTHORS.
    :license: ISC, see LICENSE for details.
"""

import os

import controlbeast.cli
import controlbeast.cli.base


class HelpCommand(controlbeast.cli.base.CbCommand):
    """
    Command class implementing the help command
    """
    def handle(self):
        """
        Command handler for the help command
        """
        if len(self._argv) > 2:
            cmd_class = controlbeast.cli.get_command(self._argv[2])
            if cmd_class:
                cmd_object = cmd_class(self._argv[2], self._executable)
                print(cmd_object.usage())
            else:
                self._status = os.EX_UNAVAILABLE
                return
        else:
            controlbeast.cli.usage(self._executable)
        self._status = os.EX_OK