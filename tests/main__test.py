from hook import main


def test_post(monkeypatch):
    test_key = 'abcde'
    monkeypatch.setenv("FLASK_POST_KEY", test_key)

    with main.app.test_client() as client:
        res = client.post('/post', data={"secret": test_key})

    assert res.status_code == 200
