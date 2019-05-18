import json
import re
import pytest

from cron import app


def test_convert():
    # assume millisecond resolution on the timestamp
    # so to convert to local time use datetime.datetime.fromtimestamp(1558070063000/1000)
    text = """
[ { DT: '/Date(1426292016000-0700)/',
 ST: '/Date(1426295616000)/',
 Trend: 4,
 Value: 101,
 WT: '/Date(1426292039000)/' } ]
    """
    expected = {'timestamp': 1426292016000, 'datetime': '03/13/2015, 17:13:36', 'trend': 4, 'direction': 'Flat', 'value': 101}
    result = app.convert(text)
    assert result == expected


def test_lambda_handler():
    pass
