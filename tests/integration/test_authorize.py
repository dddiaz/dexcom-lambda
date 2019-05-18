from cron import app


def test_authorize():
    r = app.authorize()
    assert r.status_code == 200
    print(f'Your Api Token is: {r.text}')
