# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class LeroymerlinItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()
    price = scrapy.Field()
    product_article = scrapy.Field()
    product_link = scrapy.Field()
    product_description = scrapy.Field()
    product_characters_name = scrapy.Field()
    product_characters_def = scrapy.Field()
    photo = scrapy.Field()
    product_characters_total = scrapy.Field()

    _id = scrapy.Field()


