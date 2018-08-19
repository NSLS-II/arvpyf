=================
API Documentation
=================

Start by importing  Archiver Python Frontend.

.. currentmodule:: arvpyf.mgmt

The ArchiverConfig class
-------------------------

.. autosummary::
   :toctree: generated
   :nosignatures:

   ArchiverConfig

Methods for getting the information about Archiver's PVs: 

.. autosummary::
   :toctree: generated
   :nosignatures:

   ArchiverConfig.get_all_pvs
   ArchiverConfig.get_pv_status
   ArchiverConfig.get_pv_type_info
   ArchiverConfig.get_recently_added_pvs
   ArchiverConfig.get_paused_pvs_report
   ArchiverConfig.get_never_connected_pvs

Methods for archiving PVs:

.. autosummary::
   :toctree: generated
   :nosignatures:

   ArchiverConfig.archive_pvs
   ArchiverConfig.get_archiving_status

Methods for aborting, pausing or deleting PVs:

.. autosummary::
   :toctree: generated
   :nosignatures:

   ArchiverConfig.abort_archiving_pv
   ArchiverConfig.pause_archiving_pvs
   ArchiverConfig.resume_archiving_pvs
   ArchiverConfig.delete_pv

.. currentmodule:: arvpyf.cf

The PVFinder class
--------------------

.. autosummary::
   :toctree: generated
   :nosignatures:

   PVFinder

Methods:

.. autosummary::
   :toctree: generated
   :nosignatures:


   PVFinder.get_pvs
   PVFinder.get_systems
   PVFinder.get_devices
   PVFinder.get_signals


