:orphan:

controlbeast manual page
========================

Synopsis
--------

**cb** <*command*> [*options*]


Description
-----------

:program:`cb` is a powerful tool for managing FreeBSD server configurations. It features version tracking, automated
generation of configuration files, remote deployment and bare metal installation support. It relies on proven and
well-tried methods and third-party software such as SSH and git.

Conceptually, :program:`cb` stores all configuration information within a local git repository (which can of course
be synchronized with any remote git repository using the standard git remote protocols). The meta information
required to describe a system are stored in YAML files, which allows easy editing by any common text editor.


Repository Structure
--------------------

The directory structure inside a :program:`cb` repository takes into account that several host systems shall be
manageable through the same repository. Thus, the master branch contains a host skeleton, whereas for each
host system (in short, *host*), a named branch (normally based on the master branch) shall be created. Within each host
branch, the following directory structure needs to exist by convention:

basic
   contains meta configuration files in YAML format, describing the OS version to be expected, network configuration,
   file system layout, packages, etc. The information from these files is used to compile the automatically generated
   configuration files for this system or to perform a bare metal install.

config
   contains two subdirectories, ``auto`` and ``custom``.

   auto
      is reserved for configuration files automatically generated by :program:`cb`, usually ``/boot/loader.conf``,
      ``/etc/fstab``, ``/etc/rc.conf``, ``/etc/resolv.conf`` and ``/etc/pf.conf`` (if applicable). If any of these
      files is found within the ``custom`` subdirectory, automatic generation is skipped for this specific file.

   custom
      is used for storing manually maintained configuration files. Each file's content is preceded by a YAML header,
      providing meta information such as pre and post deployment actions to be performed.

jails
   contains configuration information for jails being deployed on the respective host. Each jail is represented by
   its own subdirectory, containing the jail's configuration information stored in YAML files.


Commands
--------

commit
   Commit changes to a ControlBeast repository

help
   Display help

init
   Initialise a ControlBeast repository

new
   Create a new host within an existing ControlBeast repository

version
   Show version information
