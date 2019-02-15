import sys
import plaster

loader = plaster.get_loader(sys.argv[1], protocols=["wsgi"])
app = loader.get_wsgi_app()
server = loader.get_wsgi_server()
server(app)
