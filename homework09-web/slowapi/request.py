import dataclasses
import io
import json
import typing as tp


@dataclasses.dataclass
class Request:
    path: str
    method: str
    query: tp.Dict[str, tp.Any] = dataclasses.field(default_factory=dict)
    body: io.BytesIO = dataclasses.field(default_factory=io.BytesIO)
    headers: tp.Dict[str, str] = dataclasses.field(default_factory=dict)

    def text(self) -> tp.Optional[str]:
        # PUT YOUR CODE HERE
        pass

    def json(self) -> tp.Optional[tp.Dict[str, tp.Any]]:
        # PUT YOUR CODE HERE
        pass

