from hello_world.app import fetch

# Replace this with a current session from the auth integration test
SESSION_ID = "b3e7f4f2-3a43-4110-a359-39edd63f53c6"

# Expect the format to be of the following
# [ { DT: '/Date(1426292016000-0700)/',
#     ST: '/Date(1426295616000)/',
#     Trend: 4,
#     Value: 101,
#     WT: '/Date(1426292039000)/' } ]

# assume millisecond resolution
# so to convert to local time use datetime.datetime.fromtimestamp(1558070063000/1000)

def test_fetch():
    r = fetch()
    print(r)
    assert r is not None