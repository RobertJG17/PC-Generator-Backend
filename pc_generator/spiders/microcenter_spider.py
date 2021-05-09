import scrapy
from scrapy.loader import ItemLoader
from pc_generator.items import MicroCenterPartItem
import pandas as pd
# http://localhost:9080/crawl.json?start_requests=True&crawl_args={%22price%22:2000}&spider_name=microcenter


class MicroCenterSpider(scrapy.Spider):
    name = "microcenter"
    start_urls = ["https://www.microcenter.com/search/search_results.aspx?N=4294966937&NTK=all&sortby=match&rpp=24",
                  "https://www.microcenter.com/search/search_results.aspx?Ntk=all&sortby=match&N=4294966654&myStore=false",
                  "https://www.microcenter.com/search/search_results.aspx?Ntk=all&sortby=match&N=4294964318&myStore=false",
                  "https://www.microcenter.com/category/4294945779/ssd-solid-state-drives"]

    corresponding_ratios = {"Video Cards": .34,
                            "Power Supplies": .07,
                            "Computer Cases": .075,
                            "SSD (Solid State Drives)": .1}

    graphics_card_df = pd.DataFrame()
    power_supply_df = pd.DataFrame()
    case_df = pd.DataFrame()
    ssd_df = pd.DataFrame()

    visited_urls = []

    def parse(self, response, **kwargs):
        parts = response.css('li.product_wrapper')
        part_type = parts[0].css('a::attr(data-category)').get()

        price_point = self.price * self.corresponding_ratios[part_type]
        for part in parts:
            loader = ItemLoader(item=MicroCenterPartItem(), selector=part)
            loader.add_css(field_name='name', css='a::attr(data-name)')
            loader.add_css(field_name='price', css='a::attr(data-price)')
            loader.add_css(field_name='href', css='.normal a::attr(href)')
            loader.add_css(field_name='img', css='img::attr(src)')
            loader.add_value(field_name='part_type', value=part_type)
            # if part.css('img.imgReviews::attr(alt)') is not None:
            #     loader.add_css(field_name='rating', css='img.imgReviews::attr(alt)')
            loaded = loader.load_item()

            if loaded['price'] >= price_point:
                continue
            # yield loaded
            self.initialize_data_frame(part_type, loaded)

        next_page = response.css("ul.pages.inline a::attr(href)").getall()[-1]

        if next_page not in self.visited_urls:
            self.visited_urls.append(next_page)
            next_page = response.urljoin(next_page)
            yield response.follow(next_page, callback=self.parse)
        else:
            loaded = self.top_item(part_type)
            yield loaded
            # yield self.df.iloc[0]

    # HELPER METHODS
    def initialize_data_frame(self, part_type, loaded):
        if part_type == "Video Cards":
            self.graphics_card_df = self.graphics_card_df.append(pd.Series(loaded), ignore_index=True)
        elif part_type == "Power Supplies":
            self.power_supply_df = self.power_supply_df.append(pd.Series(loaded), ignore_index=True)
        elif part_type == "Computer Cases":
            self.case_df = self.case_df.append(pd.Series(loaded), ignore_index=True)
        elif part_type == "SSD (Solid State Drives)":
            self.ssd_df = self.ssd_df.append(pd.Series(loaded), ignore_index=True)

    def top_item(self, part_type):
        if part_type == "Video Cards":
            self.graphics_card_df.sort_values(by=['price'], ascending=False, inplace=True)
            selected = self.graphics_card_df.iloc[0].to_dict()
            loaded = self.loaded_item(selected)

        elif part_type == "Power Supplies":
            self.power_supply_df.sort_values(by=['price'], ascending=False, inplace=True)
            selected = self.power_supply_df.iloc[0].to_dict()
            loaded = self.loaded_item(selected)

        elif part_type == "Computer Cases":
            self.case_df.sort_values(by=['price'], ascending=False, inplace=True)
            selected = self.case_df.iloc[0].to_dict()
            loaded = self.loaded_item(selected)

        elif part_type == "SSD (Solid State Drives)":
            self.ssd_df.sort_values(by=['price'], ascending=False, inplace=True)
            selected = self.ssd_df.iloc[0].to_dict()
            loaded = self.loaded_item(selected)
        else:
            loaded = None

        return loaded

    def loaded_item(self, selected):
        loader = ItemLoader(MicroCenterPartItem())
        loader.add_value(field_name='name', value=selected['name'])
        loader.add_value(field_name='price', value=selected['price'])
        loader.add_value(field_name='href', value=selected['href'])
        loader.add_value(field_name='img', value=selected['img'])
        loader.add_value(field_name='part_type', value=selected['part_type'])
        # loader.add_value(field_name='rating', value=selected['rating'])
        loaded = loader.load_item()
        return loaded

