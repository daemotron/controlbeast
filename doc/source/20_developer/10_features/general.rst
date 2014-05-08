General Feature Overview
========================

The ControlBeast features refer to different stages, corresponding to different progress in deployment
of the system. The stages are:

* **Stage 0:** undefined state. Initially, a system is always assumed to be at stage 0.
* **Stage 1:** host system installed and accessible for management through ControlBeast.
* **Stage 2:** host system with package source(s) configured
* **Stage 3:** host system with packages deployed
* **Stage 4:** host system with host services deployed and running
* **Stage 5:** complete system with jails deployed

Installation
------------

Perform a basic operating system installation on the targeted system, allowing remote access via SSH
to the system.

Prerequisites
~~~~~~~~~~~~~

* System being at any stage
* Remote system booted into rescue system
* Remote system's rescue system accessible via SSH
* System configuration available in local ControlBeast repository

Expected Result: Stage 1
~~~~~~~~~~~~~~~~~~~~~~~~

* FreeBSD installed
* Custom Kernel installed (if applicable)
* SSHd configured, running and accessible for ControlBeast
* PF running and configured for host system
* Host system specific configuration files deployed

Configuration of Package Source
-------------------------------

Deploy (create, updated or delete) package source on the targeted system. The package source can either
be an external repository (such as the official FreeBSD ``pkg`` sources), or a local repository filled
by a jail offering a local `poudriere`_ service.

Prerequisites
~~~~~~~~~~~~~

* System at stage 1 or greater

Expected Result: Stage 2
~~~~~~~~~~~~~~~~~~~~~~~~

* Package source available in host system
* Packages can be created if necessary

Package Deployment
------------------

Deploy (install, update or delete) packages on the targeted host system, using the previously defined
package source. If necessary, build needed packages using `poudriere`_ before attempting to install them.

Prerequisites
~~~~~~~~~~~~~

* System at stage 2 or greater

Expected Result: Stage 3
~~~~~~~~~~~~~~~~~~~~~~~~

* Packages (independent of services, like e. g. `vim`_) installed
* Configuration specific to packages deployed (e. g. matching dotfile)

Service Deployment
------------------

Deploy (add, remove) services (host system only) by installing the required packages, deploying the appropriate
configuration files (service-specific), deploying an updated host configuration (e. g. ``rc.conf``, ``pf.conf``
etc.) and starting the services.

Prerequisites
~~~~~~~~~~~~~

* System at stage 3 or greater

Expected Result: Stage 4
~~~~~~~~~~~~~~~~~~~~~~~~

* Service packages installed
* Services configured
* Host configuration (e. g. ``rc.conf``, ``newsyslog.conf``, ``pf.conf``, etc.) adapted for services
* Services launched and running

Jail Deployment
---------------

Create jails for services to be hosted within a jailed environment, and populate the jails accordingly.

Prerequisites
~~~~~~~~~~~~~

* System at stage 4 or greater

Expected Result: Stage 5
~~~~~~~~~~~~~~~~~~~~~~~~

* Host configuration for jails deployed and activated (e. g. additional network aliases etc.)
* File systems for jails created and populated with base system (minimum: ``base.txz``)
* Packages & services inside jails installed and configured
* Jails' configuration files deployed
* Jails to be automatically started are included in ``rc.conf`` and started

Host System Update
------------------

Apply updates to the host's base system (i. e. updates coming from the FreeBSD sources itself, not
from third party packages or ports).

Prerequisites
~~~~~~~~~~~~~

* System at stage 1 or greater

Expected Result
~~~~~~~~~~~~~~~

* Updates applied to userland and kernel (if appropriate)
* If necessary, custom kernel rebuilt and installed
* Mergemaster run automatically as far as possible
* List of configuration changes which cannot automatically be merged

Host System Minor Upgrade
-------------------------

Upgrade the host's base system (i. e. only the parts coming from FreeBSD itself, not from third party
packages or ports) within the same major version (e. g. from 10.0 to 10.1).

Prerequisites
~~~~~~~~~~~~~

* System at stage 1 or greater

Expected Result
~~~~~~~~~~~~~~~

* FreeBSD sources upgraded to new branch (if appropriate)
* Upgrade applied to userland and kernel
* If necessary, custom kernel built and installed
* Mergemaster run automatically as far as possible
* List of configuration changes which cannot automatically be merged

Host System Major Upgrade
-------------------------

**Currently not supported.** In principal similar to minor upgrade, but entails also rebuild and re-installation
of all packages and services on the host system.

Package Source Jail System Update
---------------------------------

Apply updates to a package jail's base system (i. e. updates coming from the FreeBSD sources itself, not
from third party packages or ports).

Prerequisites
~~~~~~~~~~~~~

* System at stage 2 or greater

Expected Result
~~~~~~~~~~~~~~~

* Updates applied to userland
* Mergemaster run automatically as far as possible
* List of configuration changes which cannot automatically be merged

Package Source Jail Minor Upgrade
---------------------------------

Upgrade a package jail's base system (i. e. only the parts coming from FreeBSD itself, not from third party
packages or ports) within the same major version (e. g. from 10.0 to 10.1).

.. _poudriere: http://etoilebsd.net/poudriere
.. _vim: http://www.vim.org/
