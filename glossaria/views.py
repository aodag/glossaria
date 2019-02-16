from pyramid.view import view_config
from .models import Glossary, Project, Session


@view_config(route_name="top", renderer="templates/index.html")
def index(request):
    return dict()


class GlossaryView:
    def __init__(self, context, request):
        self.context = context
        self.request = request

    @property
    def project_name(self):
        return self.request.matchdict["project_name"]

    @property
    def project(self):
        return Project.query.filter(Project.name == self.project_name).first()

    @property
    def glossary_name(self):
        return self.request.matchdict["glossary_name"]

    def index(self):
        project_name = self.project_name
        glossaries = Glossary.query.filter(
            Project.name == project_name, Project.id == Glossary.project_id
        ).all()
        return dict(glossaries=glossaries)

    def detail(self):
        pass

    def new(self):
        project = self.project
        glossary = Glossary(
            name=self.request.params["name"],
            description=self.request.params["description"],
            project=project,
        )
        Session.add(glossary)
        Session.flush()
        location = self.request.route_url(
            "glossary", project_name=project.name, glossary_name=glossary.name
        )
        self.request.response.location = location
        return dict(glossary=glossary)

    def create(self):
        pass

    def edit(self):
        pass

    def update(self):
        project_name = self.project_name
        glossary_name = self.glossary_name
        glossary = Glossary.query.filter(
            Project.name == project_name,
            Project.id == Glossary.project_id,
            Glossary.name == glossary_name,
        ).first()

        params = self.request.params
        glossary.description = params["description"]
        Session.flush()

        return dict(glossary=glossary)

    def delete(self):
        project_name = self.project_name
        glossary_name = self.glossary_name
        glossary = Glossary.query.filter(
            Project.name == project_name,
            Project.id == Glossary.project_id,
            Glossary.name == glossary_name,
        ).first()
        Session.delete(glossary)
        Session.flush()
        return dict()
