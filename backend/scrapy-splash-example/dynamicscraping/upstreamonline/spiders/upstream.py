import scrapy

class UpstreamSpider(scrapy.Spider):
    name = "upstream"

    def start_requests(self):
        url = "https://www.upstreamonline.com/field-development/chinese-contractor-in-210-million-deal-to-revamp-africa-gas-field/2-1-1703068"
        yield scrapy.Request(url=url, callback=self.parse, meta={
            "splash": {
                "args": {
                    "html": 1,
                    "png": 1
                }
            }
        })

    def parse(self, response):
        print("in parse")
        print(response.data['html'])
        paragraphs = response.css("p.dn-text")
        for p in paragraphs:
            yield{
            "text":p.css("p::text").get()
              }
