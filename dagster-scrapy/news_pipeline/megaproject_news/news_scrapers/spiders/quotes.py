import scrapy


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["https://quotes.toscrape.com/"]

    def parse(self, response):
        quotes = response.css("div.quote")
        # quotes = response.xpath('//div[@class="quote"]')
        for quote in quotes:
            title = quote.css("span.text::text").get()
            # title = quote.xpath('span/text()').get()
            author = quote.css("small.author::text").get()
            # author = quote.xpath('span/small/text()').get()
            # tags = quote.css("div.tags a::text").getall()
            tags = quote.css("div.tags meta.keywords::attr('content')").get()
            yield {
                "title": title,
                "author": author,
                "tags": tags,
            }
        next_page = response.css('.next a::attr("href")').extract_first()
        if next_page:
            yield scrapy.Request(response.urljoin(next_page))
