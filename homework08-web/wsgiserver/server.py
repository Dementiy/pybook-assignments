import typing as tp

from httpserver import BaseHTTPRequestHandler, HTTPServer

from .request import WSGIRequest
from .response import WSGIResponse


class WSGIServer(HTTPServer):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.app: tp.Optional[ApplicationType] = None

    def set_app(self, app: ApplicationType) -> None:
        self.app = app

    def get_app(self) -> tp.Optional[ApplicationType]:
        return self.app


class WSGIRequestHandler(BaseHTTPRequestHandler):
    request_klass = WSGIRequest
    response_klass = WSGIResponse

    def handle_request(self, request: WSGIRequest) -> WSGIResponse:
        # сформировать словарь с переменными окружения
        # дополнить словарь информацией о сервере
        # вызвать приложение передав ему словарь с переменными окружения и callback'ом
        # ответ приложения представить в виде байтовой строки
        # вернуть объект класса WSGIResponse
        pass

