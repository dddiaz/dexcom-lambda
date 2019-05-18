from cron import app

def test_full_run():
    """Without post to dynamo, just want to make sure i can query data"""
    app.refresh_token()
    data = app.convert(app.fetch())
    print(data)
