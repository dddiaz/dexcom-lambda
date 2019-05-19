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
    result = app.convert(text)
    assert result['timestamp'] == 1426292016000
    assert result['datetime'] == '03/14/2015, 00:13:36'
    assert result['trend'] == 4
    assert result['direction'] == 'Flat'
    assert result['value'] == 101

def test_lambda_handler():
    pass
