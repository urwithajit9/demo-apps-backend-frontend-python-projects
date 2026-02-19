import scrapy
from noteapp.items import NoteappItem


class NoteSpider(scrapy.Spider):
    name = "note"
    allowed_domains = ["www.example.com"]
    start_urls = ["https://www.example.com"]

    def parse(self, response):
        print(NoteappItem)
