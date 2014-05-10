.. include:: ./stages.ref

Installation
============

Synopsis
--------

.. sourcecode:: sh

   cb install [options]

Description
-----------

The installation feature shall be used to deploy a ControlBeast-managed `FreeBSD`_ installation onto any
headless system, using the configuration information from the current ControlBeast repository branch.
Therefore, this feature can also be used for initiating a bare metal recovery.

Process Steps
-------------

==== ============= ==========================================================================================
No.  System        Description
==== ============= ==========================================================================================
01   local         **Create or update fstab** and store it within the ``conf/auto`` section of the
                   ControlBeast repository.
02   local         **Create or update minimal rc.conf** and store it within the ``conf/auto`` section of the
                   ControlBeast repository. This ``rc.conf`` file shall not start any services apart from
                   ``sshd`` (and eventually ZFS, if appropriate), but only provide a basic network and
                   system configuration.
03   local         **Create or update sshd.config** and store it within the ``conf/auto`` section of the
                   ControlBeast repository.
04   local         **Create or update loader.conf** and store it within the ``conf/auto`` section of the
                   ControlBeast repository.
05   local         **Create or update pf.conf** and store it within the ``conf/auto`` section of the
                   ControlBeast repository.
06   rescue        **Create partition scheme** on disks used for installation.
07   rescue        **Create partitions** on disks used for installation.
08   rescue        **Create disk labels** on partitions where applicable.
09   rescue        **Create file systems** on partitions or disk labels where applicable.
10   rescue        **Write boot code** either to MBR or to dedicated boot partition, depending on the
                   chosen partition scheme.
11   rescue        **Create Zpool** from partitions where applicable.
12   rescue        **Create ZFS Datasets** on Zpool where applicable and set appropriate options.
13   rescue        **Create temporary mount point** for the installation.
14   rescue        **Mount partitions and Datasets** on the temporary mount point, including ``/dev``.
                   If ZFS is used, remount file systems to generate a ``zpool.cache``.
15   rescue        **Fetch and extract FreeBSD system** packages to the temporary mount point. The minimum
                   required are ``base.txz`` and ``kernel.txz``
16   rescue        **Deploy loader.conf, zpool.cache, fstab, rc.conf, pf.conf and sshd.config** onto the
                   fresh installation at the temporary mount point.
17   rescue        **Deploy base system configuration** files from ``conf/custom`` onto the fresh
                   installation at the temporary mount point.
18   rescue        **Create ControlBeast user** in mounted environment, add it to the appropriate groups
                   and deploy a valid SSH public key in order to grant access for ControlBeast.
19   rescue        **Fetch FreeBSD Sources** for the base system and store them on the mounted system.
20   rescue        **Compile and Deploy Custom Kernel** if appropriate
21   rescue        **Unmount file systems** from temporary mount point
22   rescue        **Set mount points** for ZFS datasets where necessary
23   rescue        **Reboot** from local disk
24   local         **Verify** the server can be pinged and accessed via SSH.
25   local         **Set Stage Index** to stage|Stage Installed| if verification succeeded.
26   local         **Commit and Tag** ControlBeast repository to document the installation action
==== ============= ==========================================================================================

Required Information
--------------------

============================== =================== ===============================================================
Information                    Steps               Source
============================== =================== ===============================================================
Hard disk devices              06, 07, 08          **configuration:** ``fs.yml``
Partition Scheme               07, 08, 11          **configuration:** ``fs.yml``
Partition Mount Points         01, 11, 15, 22      **configuration:** ``fs.yml``
Zpools                         02, 12, 15          **configuration:** ``fs.yml``
ZFS Datasets                   13                  **configuration:** ``fs.yml``
ZFS Mount Points               04, 13, 15, 22, 23  **configuration:** ``fs.yml``
============================== =================== ===============================================================

.. _FreeBSD: http://www.freebsd.org/
