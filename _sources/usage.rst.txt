=====
Usage
=====

The Archiver Configuration Python Frontend (ACPF) is developed 
for extending the scope of the EPICS Archiver Appliance 
WebUI interface with a collection of methods for registering 
numerous PVs from different NSLS-II sub-systems. Its usage 
can be illustrated with the following demo.

Creating the ArchiverConfig Instance
-------------------------------------

ACPF methods are consolidated in the ArchiverConfig and PVFinder 
classes of two arvpyf submodules, mgmt and cf, respectively. 
ArchiverConfig wraps the REST API calls for cummunication with 
the Archiver MGMT server and PVFinder implements the interface 
that searches for the PVs listed in the Channel Finder dbl files. 

To create an ArchiverConfig instance, it needs to have 
a specified address of the EPICS Archiver Appliance MGMT service. 
For example, in NSLS-II, each beamline maintains its own archiver 
on a dedicated server and the corresponding address is defined in 
the /etc/archappl/appliances.xml file. Initialization of the 
PVFinder requires the path to the Channel Finder folder containing
the dbl files. 

.. code-block:: python
    
    from arvpyf import mgmt, cf
    from arvpyf.mgmt import ArchiverConfig
    from arvpyf.cf import PVFinder

    bpl_url = 'http://xf04id-ca1.cs.nsls2.local:17665/mgmt/bpl'
    arvconf = ArchiverConfig(bpl_url)

    cf_update = '/GPFS/CENTRAL/dama/cf-update/'
    pvfinder = PVFinder(cf_update)

Retrieving PVs from Archiver
----------------------------

The ArchiverConfig communication with the EPICS Archiver Appliance 
is based on a set of `business logic commands 
<https://slacmshankar.github.io/epicsarchiver_docs/api/mgmt_scriptables.html>`_
supported by the MGMT service. One of these is the getAllPV for retrieving 
all PVs from the archiver. The command has two optional arguments: 
regex and limit. The regex argument can contain a `Java regex 
<https://docs.oracle.com/javase/7/docs/api/java/util/regex/Pattern.html>`_
wildcard. The limit argument specifies the number of matched PVs that 
are returned. If unspecified, the method returns 500 PV names.

.. code-block:: python

    arv_pvs = arvconf.get_all_pvs(limit=10000)


Retrieving PVs from the Channel Finder
--------------------------------------

The PVFinder interface follows the NSLS-II Standard-Naming Convention 
defining the PV names in the form *System{Device}Signal*. For this example, 
the demo selects all PVs with '.*Mtr.*StringOut_' signals:

.. code-block:: python

    bl = "xf04"
    cf_pvs = pvfinder.get_pvs(bl, system='', device='.*', signal='.*Mtr.*StringOut_')


Selecting PVs for Archiving
---------------------------

After retrieving two PV collections from Archiver and Channel Finder 
in the same Python script, their difference can be compared, analyzed, 
and selected using standard Python methods. The demo selects 1000 PVs from 
the difference of the two collections:

.. code-block:: python

    diff_pvs = list(set(cf_pvs) - set(arv_pvs))
    demo_pvs = diff_pvs[0:1000]


Archiving PVs
-------------

In the EPICS Archiver Appliance, the PV registration is a complex procedure 
requiring several minutes for processing multiple steps. The corresponding 
request however is asynchroneous. Therefore, the demo adds a 5-minute time 
delay for processing 1000 PVs:

.. code-block:: python

    archive_pvs = arvconf.archive_pvs(demo_pvs)
    time.sleep(300)

The status of a request can be checked with the *getArchivingStatus* command. 
The present Archiver Appliance can handle a subset of PVs. Therefore, 
requests of unarchived PVs need to be aborted:

.. code-block:: python

    archived, others = arvconf.get_archiving_status(demo_pvs)
    for i, pv in enumerate(others, start=1):
        arvconf.abort_archiving_pv(pv)


Restoring the Original Test Configuration
-----------------------------------------

In order to return back to the initial test configuration, archived PVs 
need to be deleted. In the EPICS Archiver Appliance, the deleting procedure 
requires to preliminary pause the corresponding PVs. This method is also 
asynchroneous and requires a time delay. For controling this procedure, 
the test demo applies an additional *getPausedPVsReport* method:

.. code-block:: python

    paused_pvs_1 = arvconf.get_paused_pvs_report()
    pause_pvs = arvconf.pause_archiving_pvs(archived)
    time.sleep(30)
    paused_pvs_2= arvconf.get_paused_pvs_report()

Finally, paused PVs can be deleted and the status of the test configuration 
is checked with the getPausedPVsReport and getAllPVs methods:

.. code-block:: python

    for i, pv in enumerate(archived):
        delete_pv = arvconf.delete_pv(pv)
    paused_pvs = arvconf.get_paused_pvs_report()
    final_pvs = arvconf.get_all_pvs(limit=10000)

