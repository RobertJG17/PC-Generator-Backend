import scrapy
from scrapy.loader import ItemLoader
from pc_generator.items import MicroCenterPartItem
import time


class MicroCenterSpider(scrapy.Spider):
    name = "microcenter"
    start_urls = ["https://www.microcenter.com/search/search_results.aspx?N=4294966937&NTK=all&sortby=match&rpp=24",
                  "https://www.microcenter.com/search/search_results.aspx?Ntk=all&sortby=match&N=4294966654&myStore=false"]

    corresponding_ratios = {"Video Cards": .34,
                            "Power Supplies": .07}

    def parse(self, response):
        parts = response.css('li.product_wrapper')
        type_of_part = parts[0].css('a::attr(data-category)').get()
        print(type_of_part)
        price_point = self.price * self.corresponding_ratios[type_of_part]
        for part in parts:
            loader = ItemLoader(item=MicroCenterPartItem(), selector=part)
            loader.add_css(field_name='name', css='a::attr(data-name)')
            loader.add_css(field_name='price', css='a::attr(data-price)')
            loader.add_css(field_name='href', css='.normal a::attr(href)')
            loader.add_css(field_name='img', css='img::attr(src)')
            loaded = loader.load_item()
            if loaded['price'] >= price_point:
                continue
            yield loaded

        next_page = response.css("ul.pages.inline a::attr(href)").getall()[-1]

        if next_page is not None:
            next_page = response.urljoin(next_page)
            print(next_page)
            yield response.follow(next_page, callback=self.parse)

