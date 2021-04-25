import dataclasses
import typing as tp
import io

from httpserver import HTTPRequest

@dataclasses.dataclass
class WSGIRequest(HTTPRequest):
    def to_environ(self) -> tp.Dict[str, tp.Any]:
        environ = {}
        # Тут надо заполнить словарь окружения данными
        return environ
