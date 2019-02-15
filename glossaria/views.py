from pyramid.view import view_config


@view_config(route_name="top", renderer="templates/index.html")
def index(request):
    return dict()
