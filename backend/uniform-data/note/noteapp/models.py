from django.db import models
from note.dataschema import NoteSchema

NOTE = {
    'TITLE':'title'
}

# Create your models here.
class Note(models.Model):
    NOTE['TITLE'] = models.CharField(max_length=200,default="No Title")


