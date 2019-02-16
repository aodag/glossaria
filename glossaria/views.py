from pyramid.view import view_config
from pyramid.decorator import reify
from deform import Form, ValidationFailure
from .models import Glossary, Project, Session
from . import schema


@view_config(route_name="top", renderer="templates/index.html")
def index(request):
    return dict()


class GlossaryView:
    def __init__(self, context, request):
        self.context = context
        self.request = request

    @reify
    def controls(self):
        return self.request.params.items()

    @reify
    def project_name(self):
        return self.request.matchdict["project_name"]

    @reify
    def project(self):
        return Project.query.filter(Project.name == self.project_name).first()

    @reify
    def glossary_name(self):
        return self.request.matchdict["glossary_name"]

    @reify
    def glossary(self):
        return Glossary.query.filter(
            Glossary.name == self.glossary_name, Glossary.project == self.project
        ).first()

    @reify
    def new_form(self):
        return Form(schema.GlossaryNewSchema())

    @reify
    def edit_form(self):
        return Form(schema.GlossaryEditSchema())

    def collection_url(self):
        return self.request.route_url("glossaries", project_name=self.project_name)

    def member_url(self, glossary):
        return self.request.route_url(
            "glossary", project_name=glossary.project.name, glossary_name=glossary.name
        )

    def index(self):
        project_name = self.project_name
        glossaries = Glossary.query.filter(
            Project.name == project_name, Project.id == Glossary.project_id
        ).all()
        return dict(glossaries=glossaries)

    def detail(self):
        return dict(glossary=self.glossary)

    def edit(self):
        return dict(glossary=self.glossary, form=self.edit_form)

    def new(self):
        return dict(form=self.new_form)

    def create(self):
        try:
            params = self.new_form.validate(self.controls)
        except ValidationFailure as e:
            return dict(form=e.field)

        project = self.project
        glossary = Glossary(
            name=params["name"], description=params["description"], project=project
        )
        Session.add(glossary)
        Session.flush()
        location = self.member_url(glossary)
        self.request.response.location = location
        return dict(glossary=glossary)

    def update(self):
        try:
            params = self.edit_form.validate(self.controls)
        except ValidationFailure as e:
            return dict(form=e.field)

        glossary = self.glossary
        glossary.description = params["description"]
        Session.flush()

        location = self.member_url(glossary)
        self.request.response.location = location

        return dict(glossary=glossary)

    def delete(self):
        glossary = self.glossary
        Session.delete(glossary)
        Session.flush()
        location = self.collection_url()
        self.request.response.location = location
        return dict()
