import pytest


@pytest.fixture
def settings():
    return {}


@pytest.fixture
def app(monkeypatch, settings):
    import webtest
    from glossaria import main

    monkeypatch.setattr("pyramid_sqlalchemy.includeme", lambda c: None)
    app = main({}, **settings)
    return webtest.TestApp(app, extra_environ={"repoze.tm.active": True})


def test_index(app):
    res = app.get("/")
    assert "Hello" in res
