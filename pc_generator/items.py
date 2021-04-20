# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html


from scrapy.item import Item, Field
from scrapy.loader.processors import MapCompose, TakeFirst
from datetime import datetime


def remove_quotes(text):
    # strip the unicode quotes
    text = text.strip(u'\u201c'u'\u201d')
    return text


def convert_date(text):
    # convert string March 14, 1879 to Python date
    return datetime.strptime(text, '%B %d, %Y')


def parse_location(text):
    # parse location "in Ulm, Germany"
    return text[3:]


def price_to_float(string):
    return float(string)


def microcenter_append_href(text):
    return 'https://www.microcenter.com' + text


# def format_rating(rating):
#     print(rating)
#     return float(rating[0])


class MicroCenterPartItem(Item):
    name = Field(
        output_processor=TakeFirst()
    )
    price = Field(
        input_processor=MapCompose(price_to_float),
        output_processor=TakeFirst()
    )
    href = Field(
        input_processor=MapCompose(microcenter_append_href),
        output_processor=TakeFirst()
    )
    img = Field(
        output_processor=TakeFirst()
    )
    part_type = Field(
        output_processor=TakeFirst()
    )


class QuoteItem(Item):
    quote_content = Field(
        input_processor=MapCompose(remove_quotes),
        # TakeFirst return the first value not the whole list
        output_processor=TakeFirst()
    )
    author_name = Field(
        input_processor=MapCompose(str.strip),
        output_processor=TakeFirst()
    )
    author_birthday = Field(
        input_processor=MapCompose(convert_date),
        output_processor=TakeFirst()
    )
    author_born_location = Field(
        input_processor=MapCompose(parse_location),
        output_processor=TakeFirst()
    )
    author_bio = Field(
        input_processor=MapCompose(str.strip),
        output_processor=TakeFirst()
    )
    tags = Field()


