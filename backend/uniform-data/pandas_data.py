import pandas as pd
from note.note.dataschema import NoteSchema

df = pd.DataFrame(columns=NoteSchema.list())

print(NoteSchema.TAGS)

print(NoteSchema.list())

df[NoteSchema.CONTENT] = [1, 2, 3]
print(df)