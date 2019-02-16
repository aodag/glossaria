from pyramid import testing
import pytest


@pytest.fixture
def config():
    yield testing.setUp()
    testing.tearDown()


@pytest.fixture
def models(sql_session):
    from glossaria import models

    sql_session.bind.echo = True
    models.BaseObject.metadata.create_all(bind=sql_session.bind)
    yield models
    models.BaseObject.metadata.drop_all(bind=sql_session.bind)


def test_index():
    from glossaria.views import index

    request = testing.DummyRequest()
    result = index(request)
    assert result == {}


class TestGlossaryView:
    @pytest.fixture
    def target(self):
        from glossaria.views import GlossaryView

        return GlossaryView

    def test_index(self, target, models, sql_session):
        project1 = models.Project(name="testing")
        sql_session.add(project1)
        project2 = models.Project(name="other")
        sql_session.add(project2)
        glossary1 = models.Glossary(name="g1", project=project1)
        models.Glossary(name="g2", project=project2)
        sql_session.flush()

        request = testing.DummyRequest(matchdict={"project_name": project1.name})
        context = testing.DummyResource()
        view = target(context, request)
        result = view.index()
        assert result == {"glossaries": [glossary1]}

    def test_create(self, target, models, sql_session, config):
        project1 = models.Project(name="testing")
        sql_session.add(project1)
        sql_session.flush()
        config.add_route("glossary", "/glossaries/{project_name}/{glossary_name}")

        params = dict(name="testing glossary", description="this is testing glossary")

        request = testing.DummyRequest(
            matchdict={"project_name": project1.name}, params=params
        )
        context = testing.DummyResource()
        view = target(context, request)
        result = view.create()
        assert result["glossary"].name == "testing glossary"
        g = sql_session.query(models.Glossary).filter_by(name=params["name"]).one()
        assert g == result["glossary"]
        assert g.project == project1
        assert (
            request.response.location
            == "http://example.com/glossaries/testing/testing%20glossary"
        )

    def test_update(self, target, models, sql_session, config):
        glossary1 = models.Glossary(name="glossary1")
        project1 = models.Project(name="testing", glossaries=[glossary1])
        sql_session.add(project1)
        sql_session.flush()
        config.add_route("glossary", "/glossaries/{project_name}/{glossary_name}")

        params = dict(name="testing glossary", description="this is testing glossary")

        request = testing.DummyRequest(
            matchdict={"project_name": project1.name, "glossary_name": glossary1.name},
            params=params,
        )
        context = testing.DummyResource()
        view = target(context, request)
        result = view.update()
        assert result == {"glossary": glossary1}
        assert glossary1.description == "this is testing glossary"

    def test_delete(self, target, models, sql_session, config):
        from sqlalchemy import inspect

        config.add_route("glossaries", "/glossaries/{project_name}")

        glossary1 = models.Glossary(name="glossary1")
        project1 = models.Project(name="testing", glossaries=[glossary1])
        sql_session.add(project1)
        sql_session.flush()

        request = testing.DummyRequest(
            matchdict={"project_name": project1.name, "glossary_name": glossary1.name}
        )
        context = testing.DummyResource()
        view = target(context, request)
        result = view.delete()
        assert result == {}
        assert inspect(glossary1).deleted
        assert request.response.location == "http://example.com/glossaries/testing"

    def test_detail(self, target, models, sql_session, config):
        glossary1 = models.Glossary(name="glossary1")
        project1 = models.Project(name="testing", glossaries=[glossary1])
        sql_session.add(project1)
        sql_session.flush()

        request = testing.DummyRequest(
            matchdict={"project_name": project1.name, "glossary_name": glossary1.name}
        )
        context = testing.DummyResource()
        view = target(context, request)
        result = view.detail()
        assert result == {"glossary": glossary1}

    def test_edit(self, target, models, sql_session, config):
        glossary1 = models.Glossary(name="glossary1")
        project1 = models.Project(name="testing", glossaries=[glossary1])
        sql_session.add(project1)
        sql_session.flush()

        request = testing.DummyRequest(
            matchdict={"project_name": project1.name, "glossary_name": glossary1.name}
        )
        context = testing.DummyResource()
        view = target(context, request)
        result = view.edit()
        assert result == {"glossary": glossary1, "form": view.edit_form}

    def test_new(self, target, models, sql_session, config):
        project1 = models.Project(name="testing")
        sql_session.add(project1)
        sql_session.flush()

        request = testing.DummyRequest(matchdict={"project_name": project1.name})
        context = testing.DummyResource()
        view = target(context, request)
        result = view.new()
        assert result == {"form": view.new_form}
