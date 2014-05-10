.. include:: ./stages.ref

Purging
=======

Synopsis
--------

.. sourcecode:: sh

   cb purge [options]

Description
-----------

The purge feature shall be used to cleanse any residual data from the targeted system,
transforming it into a state ready for installation (Stage |Stage Purged|).

Process Steps
-------------

==== ============= ==========================================================================================
No.  System        Description
==== ============= ==========================================================================================
01   rescue        **Cleanse hard disks** by copying binary zero's from ``/dev/zero`` onto the device. For
                   flash memory devices (such as SSD disks), only overwrite the boot sector and partition
                   table. For classic hard disks, overwrite the full disk.
02   rescue        **Verify** that disk's MBRs are cleaned and ``dd`` processes terminated
03   local         **Set Stage Index** to stage |Stage Purged| if verification succeeded, otherwise to stage
                   |Stage Undefined|.
==== ============= ==========================================================================================

Required Information
--------------------

============================== =================== ===============================================================
Information                    Steps               Source
============================== =================== ===============================================================
List of hard disk devices      01, 02              **configuration:** ``fs.yml``
Type of hard disk device       01                  **configuration:** ``fs.yml``
Remote Host (IP or FQDN)       01, 02              **configuration:** ``rescue.yml``
Remote Host User               01, 02              **configuration:** ``rescue.yml``
Remote Host Auth Method        01, 02              **configuration:** ``rescue.yml``
Remote Host Password           01, 02              **configuration:** ``rescue.yml``
Remote Host Public Key         01, 02              **convention:** first look for
                                                   :py:meth:`~controlbeast.ssh.agent.CbSSHAgent.keys`; then (if
                                                   none found) look for ``id_*`` files in ``~/.ssh/``. Can be
                                                   overridden by command line option.
Remote Host Pubkey Password    01, 02              **runtime:** detect ``ssh-agent`` or query from user interface
============================== =================== ===============================================================