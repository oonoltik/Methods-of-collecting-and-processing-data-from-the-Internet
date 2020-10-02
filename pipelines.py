# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import scrapy
from pymongo import MongoClient
from scrapy.pipelines.images import ImagesPipeline

class InstaparserPipeline:
    def __init__(self):
        client = MongoClient('localhost',27017)
        #client.drop_database('instagram_base')
        self.mongo_base = client.instagram_base

    def process_item(self, item_post, spider):
        print("New post")
        collection = self.mongo_base[spider.name + 'post']
        collection.insert_one(item_post)
        return item_post

    def process_item(self, item_follower, spider):
        print("New follower")
        collection = self.mongo_base[spider.name + 'follower']
        collection.insert_one(item_follower)
        return item_follower