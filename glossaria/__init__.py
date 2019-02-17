from pyramid.config import Configurator


def includeme(config):
    config.add_route("top", "/")
    config.add_route("glossaries.index", "/glossaries")
    config.add_route("glossaries.new", "/glossaries/new/{project_name}")
    config.add_route("glossaries.create", "/glossaries/create/{project_name}")
    config.add_route(
        "glossaries.detail", "/glossaries/detail/{project_name}/{glossary_name}"
    )
    config.add_route(
        "glossaries.edit", "/glossaries/edit/{project_name}/{glossary_name}"
    )
    config.add_route(
        "glossaries.update", "/glossaries/update/{project_name}/{glossary_name}"
    )
    config.add_route(
        "glossaries.delete", "/glossaries/delete/{project_name}/{glossary_name}"
    )
    config.scan(".views")


def main(global_conf, **settings):
    config = Configurator(settings=settings)
    config.include("pyramid_tm")
    config.include("pyramid_sqlalchemy")
    config.include("pyramid_jinja2")
    config.add_jinja2_renderer(".html")
    config.include(".")
    return config.make_wsgi_app()
