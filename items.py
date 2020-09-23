# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst



def price_to_int(price):
    if price:

        try:
            price = price.replace('.00', '')
            return int(price)
        except:
            price = price
    else:
        price = 0
    return price

class LeroymerlinItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()
    price = scrapy.Field(input_processor=MapCompose(price_to_int),output_processor=TakeFirst())
    product_article = scrapy.Field()
    product_link = scrapy.Field()
    product_description = scrapy.Field()
    product_characters_name = scrapy.Field()
    product_characters_def = scrapy.Field()
    photo = scrapy.Field()
    product_characters_total = scrapy.Field()

    _id = scrapy.Field()

# class AvitoparserItem(scrapy.Item):
#     # define the fields for your item here like:
#     name = scrapy.Field(output_processor=TakeFirst())
#     price = scrapy.Field(input_processor=MapCompose(price_to_int), output_processor=TakeFirst())
#     # price = scrapy.Field()
#     photo = scrapy.Field()
#     _id = scrapy.Field()
#     # ads_link = scrapy.Field()



