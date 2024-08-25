from enum import Enum
from pydantic import BaseModel


class Catergory(Enum):
    ENTRY = "Entry"


class Entry(BaseModel):
    name: str
    content: str
    id_num: int
