from dataclasses import field
from typing import List, Optional

from marshmallow_dataclass import dataclass


@dataclass
class Product:
    id: str = field(metadata={"required": True})
    oids: List[str] = field(default_factory=list)
    name: str = ""
