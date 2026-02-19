#from enum import StrEnum #python 3.11
from strenum import StrEnum
from enum import auto
from strenum import LowercaseStrEnum, UppercaseStrEnum

# class NoteSchema(StrEnum):

#     TITLE = "title"
#     CONTENT = "content"
#     TAGS = "tags"

#     @classmethod
#     def list(cls):
#         return list(map(lambda c: c.value, cls))


class NoteSchema(LowercaseStrEnum):
    TITLE = auto()
    CONTENT = auto()
    TAGS = auto()

print(NoteSchema.TITLE)
