# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class JobparserItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    salary = scrapy.Field()
    min_salary = scrapy.Field()
    max_salary = scrapy.Field()
    curency = scrapy.Field()
    vacancy_link = scrapy.Field()
    site_name = scrapy.Field()


    salary_comment = scrapy.Field()
    _id = scrapy.Field()
