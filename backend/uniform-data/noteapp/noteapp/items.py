# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from note.note.dataschema import NoteSchema


class NoteappItem(scrapy.Item):
    # define the fields for your item here like:
    NoteSchema.TITLE.__str__ = scrapy.Field()
    NoteSchema.CONTENT.__str__ = scrapy.Field()
    NoteSchema.TAGS.__str__ = scrapy.Field()

