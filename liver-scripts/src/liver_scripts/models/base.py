import copy
from collections.abc import Callable
from dataclasses import dataclass, fields
from typing import TypeVar

T = TypeVar("T")


@dataclass
class BaseModel:
    def _copydict(self, copyfunc: Callable[[T], T]):
        return {
            name: copyfunc(getattr(self, name))
            for name in (f.name for f in fields(self))
        }

    def __copy__(self):
        data = self._copydict(copy.copy)
        return type(self)(**data)

    def __deepcopy__(self, memo):
        data = self._copydict(lambda v: copy.deepcopy(v, memo))
        return type(self)(**data)


@dataclass
class BaseDependent:
    name: str
    parents: list[str]
