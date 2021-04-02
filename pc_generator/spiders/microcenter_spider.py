import scrapy
from scrapy.loader import ItemLoader
from pc_generator.items import MicroCenterPartItem
import time


class MicroCenterSpider(scrapy.Spider):
    name = "microcenter"
    start_urls = ["https://www.microcenter.com/search/search_results.aspx?N=4294966937&NTK=all&sortby=match&rpp=24"]

    def parse(self, response):
        parts = response.css('li.product_wrapper')

        for part in parts:
            loader = ItemLoader(item=MicroCenterPartItem(), selector=part)
            loader.add_css(field_name='name', css='a::attr(data-name)')
            loader.add_css(field_name='price', css='a::attr(data-price)')
            loader.add_css(field_name='href', css='.normal a::attr(href)')
            loader.add_css(field_name='img', css='img::attr(src)')
            yield loader.load_item()

            # yield {
            #     'name': part.css('a::attr(data-name)').get(),
            #     'price': part.css('a::attr(data-price)').get(),
            #     'href': part.css('.normal a::attr(href)').get(),
            #     'img': part.css('img::attr(src)').get()
            # }

            # author_url = parts.css('.author + a::attr(href)').get()
            #
            # self.logger.info("get author page url")
            # yield response.follow(author_url, callback=self.parse_author, meta={'quote_item': quote_item})

        # next_page = response.css('li.next a::attr(href)').get()
        # if next_page is not None:
        #     next_page = response.urljoin(next_page)
        #     yield scrapy.Request(next_page, callback=self.parse)

        next_page = response.css("ul.pages.inline a::attr(href)").getall()[-1]

        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield response.follow(next_page, callback=self.parse)

    #
    # def parse_author(self, response):
    #     quote_item = response.meta['quote_item']
    #     loader = ItemLoader(item=quote_item, response=response)
    #     loader.add_css('author_name', '.author-title::text')
    #     loader.add_css('author_birthday', '.author-born-date::text')
    #     loader.add_css('author_born_location', '.author-born-location::text')
    #     loader.add_css('author_bio', '.author-description::text')
    #     yield loader.load_item()
