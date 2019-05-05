# from __future__ import (absolute_import, division, print_function,
#                        unicode_literals)

import logging
from pathlib import Path
import vcr as _vcr

from arvpyf.ar import ArchiverReader

# VCR

cassette_library_dir = str(Path(__file__).parent / Path('cassettes'))

vcr = _vcr.VCR(
        serializer='json',
        cassette_library_dir=cassette_library_dir,
        record_mode='once',
        match_on=['method'],
)

logging.basicConfig()
vcr_log = logging.getLogger("vcr")
vcr_log.setLevel(logging.INFO)

# Archiver Reader

ar_url = 'http://localhost:17668'
ar_tz = 'US/Eastern'

config = {'url': ar_url, 'timezone': ar_tz}

arvReader = ArchiverReader(config)

# ArchiverReader VCR-based Test

pv = 'XF:23ID-ID{BPM}Val:PosXS-I'
since = '2016-10-06 17:55:35'
until = '2016-10-06 17:54:35'


@vcr.use_cassette()
def test_get():
    df = arvReader.get(pv, since, until)
    assert len(df) == 61
    assert round(df.data[60], 6) == 0.004321
    assert df.time[60].strftime('%Y-%m-%d %H:%M:%S') == '2016-10-06 17:54:34'
    return df

# df = test_get()
# print(df)
