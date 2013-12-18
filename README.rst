ControlBeast
============

.. image:: https://secure.travis-ci.org/daemotron/controlbeast.png?branch=master
   :target: http://travis-ci.org/daemotron/controlbeast
   :alt: Travis-ci: continuous integration status.

ControlBeast is a command line based software helping FreeBSD_ system administrators with automatizing 
repetitive tasks and managing all information related to a server's configuration in one place. ControlBeast 
has been developed with security in mind, but also following the KISS_ principle – unnecessary complexity has
always been one of the most common sources for security issues.

ControlBeast heavily relies on YAML_ to store all kinds of configuration information, making it easy to edit
and also later understand them. This approach allows maintaining the whole configuration information within a
version management system. Git_, one of the most powerful distributed SCM systems has been chosen for this
purpose, building a strong basis for many of ControlBeast's features.

Speaking of features, among many others, the following ones offered by ControlBeast are probably worth mentioning:

* Secure remote deployment mechanism via SSH ensures configuration integrity of the managed system
* Bare metal (re–)install functionality allows cloning of an existing system onto a new machine, disaster recovery, etc.
* Support of FreeBSD's jails for virtualisation purposes.

ControlBeast is licensed under the terms of the `ISC License`_. ControlBeast is free software; you are free to
change and redistribute it. However, there is no warranty, to the extent permitted by law.

.. _FreeBSD: http://www.freebsd.org/
.. _KISS: http://en.wikipedia.org/wiki/KISS_principle
.. _YAML: http://yaml.org/
.. _Git: http://git-scm.com/
.. _ISC License: http://www.opensource.org/licenses/isc-license.txt
