=========
Retrieval
=========

EPICS Archiver Appliance data retrieval is based on REST API.

Creating the ArchiverReader Instance
-------------------------------------

An ArchiverReader instance is created by specifing the Archiver
Retrieval service address and time zone: 

.. code-block:: python

    from arvpyf.ar import ArchiverReader

    ar_url = 'http://xf23id-ca.cs.nsls2.local:17668'
    ar_tz = 'US/Eastern'

    config = {'url': ar_url, 'timezone': ar_tz}

    arvReader = ArchiverReader(config)


Data Retrieval
--------------

The data retrieval interface is encapsulated in the get() method using
three arguments: EPICS PV name and the start/end times. As a result,
the method returns a pandas.DataFrame with the time and data columns.  

.. code-block:: python

    pv = 'XF:23ID-ID{BPM}Val:PosXS-I'
    since = '2016-10-06 17:55:35'
    until = '2016-10-06 17:54:35'

    df = arvReader.get(pv, since, until)

