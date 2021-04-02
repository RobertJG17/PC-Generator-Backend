import scrapy
from pc_generator import items
from scrapy.loader import ItemLoader
from pc_generator.items import QuoteItem


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = ["http://quotes.toscrape.com/"]

    def parse(self, response):
        self.logger.info("YOYOYOYO")

        quotes = response.css('div.quote')

        for quote in quotes:
            loader = ItemLoader(item=QuoteItem(), selector=quote)
            loader.add_css(field_name='quote_content', css='.text::text')
            loader.add_css(field_name='tags', css='.tag::text')
            quote_item = loader.load_item()

            # yield {
            #     'text': quote.css('.text::text').get(),
            #     'author': quote.css('.author::text').get(),
            #     'tags': quote.css('.tag::text').getall()
            # }

            author_url = quote.css('.author + a::attr(href)').get()

            self.logger.info("get author page url")
            yield response.follow(author_url, callback=self.parse_author, meta={'quote_item': quote_item})

        # next_page = response.css('li.next a::attr(href)').get()
        # if next_page is not None:
        #     next_page = response.urljoin(next_page)
        #     yield scrapy.Request(next_page, callback=self.parse)

        for a in response.css('li.next a'):
            yield response.follow(a, callback=self.parse)

    def parse_author(self, response):
        quote_item = response.meta['quote_item']
        loader = ItemLoader(item=quote_item, response=response)
        loader.add_css('author_name', '.author-title::text')
        loader.add_css('author_birthday', '.author-born-date::text')
        loader.add_css('author_born_location', '.author-born-location::text')
        loader.add_css('author_bio', '.author-description::text')
        yield loader.load_item()
