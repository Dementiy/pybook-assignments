import dataclasses
import re
import typing as tp


@dataclasses.dataclass
class Route:
    path: str
    method: str
    func: tp.Callable

