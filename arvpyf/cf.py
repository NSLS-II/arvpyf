import glob
import re


class PVFinder(object):
    """
    Interface to the Channel Finder dbl files
    using the PV System{Device}Signal naming convention
    """
    def __init__(self, cf_update):
        """
        Constructor

        Parameters
        ----------
        cf_update : str
            name of the Channel Finder directory
        """
        self.cf_update = cf_update

    def get_pvs(self, beamline, system='', device='.*', signal='.*'):
        """
        Return PV names for the selected beamline, system, device, and signals

        Parameters
        ----------
        beamline : str
            beamline name
        system: str, optional
            regular expression, default: '.*'
        device: str, optional
            regular expression, default: '.*'
        signal: str, optional
            regular expression, default: .*'

        Returns
        -------
        list : list of PV names
        """
        files = glob.glob(self.cf_update + "*.dbl")

        # select the beamline files
        bl_files = [s for s in files if beamline in s]

        pattern = '.*' + system + '{' + device + '}' + signal  # + '\Z'

        pvs = []
        for fname in bl_files:
            f = open(fname, 'r')
            f_pvs = [pv.rstrip('\n') for pv in f]
            p_pvs = [pv for pv in f_pvs if re.match(pattern, pv)]
            pvs += p_pvs
            f.close()

        return pvs

    def get_systems(self, pvs):
        """
        Return PV system names

        Parameters
        ----------
        pvs : list
            list of PV names
        """
        list_systems = [s[:s.find('{')] for s in pvs]
        return list_systems

    def get_devices(self, pvs):
        """
        Return PV device names

        Parameters
        ----------
        pvs : list
            list of PV names
        """
        list_devices = [s[s.find('{')+1: s.find('}')] for s in pvs]
        return list_devices

    def get_signals(self, pvs):
        """
        Return PV signal names

        Parameters
        ----------
        pvs : list
            list of PV names
        """
        list_signals = [s[s.find('}')+1:] for s in pvs]
        return list_signals
