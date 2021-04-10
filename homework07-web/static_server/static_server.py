import mimetypes
import pathlib
import time
import typing as tp
from urllib.parse import unquote, urlparse

from httpserver import BaseHTTPRequestHandler, HTTPRequest, HTTPResponse, HTTPServer


def url_normalize(path: str) -> str:
    pass


class StaticHTTPRequestHandler(BaseHTTPRequestHandler):
    def handle_request(self, request: HTTPRequest) -> HTTPResponse:
        # NOTE: https://tools.ietf.org/html/rfc3986
        # NOTE: echo -n "GET / HTTP/1.0\r\n\r\n" | nc localhost 5000
        pass


class StaticServer(HTTPServer):
    pass


if __name__ == "__main__":
    document_root = pathlib.Path("static") / "root"
    server = StaticServer(
        timeout=60,
        document_root=document_root,
        request_handler_cls=StaticHTTPRequestHandler,
    )
    server.serve_forever()
