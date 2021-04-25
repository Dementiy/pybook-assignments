import sys

from .server import WSGIRequestHandler, WSGIServer

if __name__ == "__main__":
    app_path = sys.argv[1]
    module, application = app_path.split(":")
    module = __import__(module)
    app = getattr(module, application)
    server = WSGIServer(request_handler_cls=WSGIRequestHandler)
    server.set_app(app)
    server.serve_forever()
