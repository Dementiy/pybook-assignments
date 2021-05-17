import dataclasses
import json
import typing as tp


@dataclasses.dataclass
class Response:
    content_type: tp.ClassVar[tp.Optional[str]] = None
    status: int
    headers: tp.Dict[str, str] = dataclasses.field(default_factory=dict)
    body: tp.Optional[tp.Any] = None


@dataclasses.dataclass
class JsonResponse(Response):
    content_type: tp.ClassVar[str] = "application/json"
    data: tp.Dict[str, tp.Any] = dataclasses.field(default_factory=dict)
    status: int = 200
    serializer: tp.Optional[tp.Callable] = None

