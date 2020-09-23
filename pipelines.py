# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface

import scrapy
from pymongo import MongoClient
from scrapy.pipelines.images import ImagesPipeline

class LeroymerlinPipeline:

    def __init__(self):
        client = MongoClient('localhost',27017)
        #client.drop_database('leroymerlin_base')
        self.mongo_base = client.leroymerlin_base

    def process_item(self, item, spider):
        row_2 = []
        for i in item['product_characters_def']:
            i = i.replace('\n', '')
            i = i.replace('  ', '')
            row_2.append(i)
            item['product_characters_def'] = row_2

        keys = item['product_characters_name']
        values = item['product_characters_def']


        item['product_characters_total'] = dict(zip(keys, values))



        collection = self.mongo_base[spider.name]
        collection.insert_one(item)
        return item

class LeroymerlinPhotosPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if item['photo']:
            for img in item['photo']:
                yield scrapy.Request(img, meta={'product_url':item['product_link']})

    def file_path(self, request, response=None, info=None):
        product_url = request.meta['product_url']
        folder = product_url.split('/')[-2]
        file_name = request.url.split('/')[-1]
        return folder + '/' + file_name


    def item_completed(self, results, item, info):
        if results:
            item['photo'] = [itm[1] for itm in results if itm[0]]
        return item

    print()