# -*- coding: utf-8 -*-
"""
    controlbeast.cli.base
    ~~~~~~~~~~~~~~~~~~~~~

    :copyright: Copyright 2013 by the ControlBeast team, see AUTHORS.
    :license: ISC, see LICENSE for details.
"""


import argparse
import os


class CbCommand(object):
    """
    The base class from which all ControlBeast commands derive.

    Attributes affecting the behaviour of a Command object:

    ``_help``
        A short description of the command, which will be used
        to construct help messages or usage instructions for the
        command.

    ``_arg_list``
        A tuple of arguments accepted by the command. Each argument
        consists of a tuple with two elements.
        The first element is a tuple containing the short and long
        option identifiers; e. g. ('-f', '--foo')
        The second element is a dictionary containing arbitrary elements.
        All keyword arguments accepted by :py:func:`argparse.ArgumentParser.add_argument`
        are allowed as key names within this dictionary.
    """

    _help = ''
    _arg_list = ()

    def __init__(self, command, executable):
        self._status = 0
        self._command = command
        self._executable = os.path.basename(executable)


    def usage(self):
        """
        Generate a usage message for the command
        """
        umsg = None
        if self._arg_list:
            umsg = "usage: %s %s [options]" % (self._executable, self._command)
        else:
            umsg = "usage: %s %s" % (self._executable, self._command)
        if self._help:
            umsg += "\n\n%s" % self._help
        if self._arg_list:
            umsg += "\n\nAvailable options:\n"
            for arg in self._arg_list:
                if len(arg) > 1:
                    if 'help' in arg[1]:
                        umsg += "  {: <15s}   {: <60s}\n".format(', '.join(arg[0]), arg[1]['help'])
                    else:
                        umsg += "  {: <15s}   {: <60s}\n".format(', '.join(arg[0]), 'no description available')
                elif len(arg) == 1:
                    umsg += "  {: <15s}   {: <60s}\n".format(', '.join(arg[0]), 'no description available')
        return umsg


    def execute(self, argv):
        """
        Process arguments submitted on the command line and
        provide internal parser structures. Then call the
        handle() method which needs to be implemented by each
        ControlBeast command.
        """
        self._argv = argv
        if self._arg_list:
            parser = argparse.ArgumentParser(self._executable, add_help=False, usage=self.usage()[7:])
            for arg in self._arg_list:
                parser.add_argument(*arg[0], **arg[1])
            self._args = parser.parse_args(argv[2:])
        else:
            self._args = None
        self.handle()


    def handle(self):
        """
        The handle method contains the actual code for the command.
        This method needs to be implemented for each command.
        """
        self._status = -1
        raise NotImplementedError()


    @property
    def status(self):
        return self._status


    @property
    def help(self):
        return self._help
