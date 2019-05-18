from cron.app import fetch

# Note this file relies on a global variable defined in the app.py file for SESSION_ID.


def test_fetch():
    r = fetch()
    print(r)
    assert r is not None