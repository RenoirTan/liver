from __future__ import annotations
from typing import *
from . import utils


class TokenColor(Hashable):
    def __init__(self, config: Dict) -> None:
        self.name: str = config["name"]
        self.scope: List[str] = config["scope"]
        self.settings: str = config["settings"]
    
    def __hash__(self) -> int:
        return hash(self.name)
    
    def __eq__(self, other: TokenColor) -> bool:
        return self.name == other.name
    
    def to_dict(self) -> Dict:
        return {
            "name": self.name,
            "scope": self.scope,
            "settings": self.settings
        }
