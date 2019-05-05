import datetime as dt
import pytz
import numpy as np
import pandas as pd
import requests


class ArchiverReader(object):

    def __init__(self, config):

        if all(k in config for k in ['url', 'timezone']):
            pass
        else:
            raise TypeError("config {} does not include one of required"
                            " keys (url, timezone).".format(config))

        url = config['url']
        if not url.endswith('/'):
            url += '/'
        self.url = url
        self.archiver_addr = self.url + "retrieval/data/getData.json"

        self.timezone = config['timezone']
        self.tz = pytz.timezone(self.timezone)

    def get(self, pv, since, until):

        _since = dt.datetime.strptime(since, '%Y-%m-%d %H:%M:%S')
        _until = dt.datetime.strptime(until, '%Y-%m-%d %H:%M:%S')
        _from = self.tz.localize(_since).replace(microsecond=0).isoformat()
        _to = self.tz.localize(_until).replace(microsecond=0).isoformat()

        params = {'pv': pv, 'from': _from, 'to': _to}

        req = requests.get(self.archiver_addr, params=params, stream=True)
        req.raise_for_status()

        # process data

        raw, = req.json()

        secs = [x['secs'] for x in raw['data']]
        nanos = [x['nanos'] for x in raw['data']]
        data = [x['val'] for x in raw['data']]

        asecs = np.asarray(secs)
        ananos = np.asarray(nanos)
        times = asecs*1.0e+3 + ananos*1.0e-6
        datetimes = pd.to_datetime(times, unit='ms')

        # create the DataFrame

        df = pd.DataFrame()

        df['time'] = datetimes
        df['data'] = data

        df.time = df.time.dt.tz_localize('UTC').dt.tz_convert(self.timezone)

        return df
