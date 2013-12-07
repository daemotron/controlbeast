# -*- coding: utf-8 -*-
"""
    controlbeast.cli
    ~~~~~~~~~~~~~~~~

    :copyright: Copyright 2013 by the ControlBeast team, see AUTHORS.
    :license: ISC, see LICENSE for details.
"""
import os

from controlbeast.cli.base import CbCommand
from controlbeast.utils import loader


_commands = None


def load_commands():
    """
    Detect available command modules or packages and store result in _commands variable
    """
    global _commands
    cmds = loader.detect_class_modules('controlbeast.cli', parent=CbCommand)
    _commands = {}
    for cmd in cmds:
        _commands[cmds[cmd].split('.')[-1]] = [cmd, cmds[cmd]]


def get_command(command_name):
    """
    Get a command class by its name

    :param str command_name: The name of the command class to be loaded
    :return: command class reference which can be instantiated
    """
    global _commands
    if not _commands:
        load_commands()

    if not _commands:
        return None

    if command_name in _commands:
        return loader.load_member(_commands[command_name][1], _commands[command_name][0])
    else:
        return None


def usage(executable):
    """
    Print a global usage message

    :param str executable: Name of the executable
    """
    global _commands
    if not _commands:
        load_commands()

    print("""Usage: %s <command> [options]

Type '%s help <command>' for help on a specific command.""" % (
        os.path.basename(executable), os.path.basename(executable)
    ))
    if _commands:
        print("\nAvailable commands:")
        for i in sorted(_commands.keys()):
            print("  %s" % i)


def dispatch(executable, argv):
    """
    Function being called from the executable to launch the CLI.
    This is the initial entrance point for any ControlBeast processing.

    :param str executable: Name of the executable
    :param list argv: vector with command line arguments
    """
    if len(argv) > 1:
        cmd_class = get_command(argv[1])
        if cmd_class:
            cmd_object = cmd_class(argv[1], executable)
            cmd_object.execute(argv)
            return cmd_object.status
        else:
            return os.EX_UNAVAILABLE
    else:
        usage(executable)
        return os.EX_USAGE
