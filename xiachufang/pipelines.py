# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
from instapush import App


class MongoPipeline(object):
    collection_name = "recipe_item"

    def __init__(self, mongo_uri, mongo_db, instapush_appid, instapush_secret):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.instapush_app = None
        if instapush_appid and instapush_secret:
            self.instapush_app = App(appid=instapush_appid, secret=instapush_secret)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get("MONGO_URI"),
            mongo_db=crawler.settings.get("MONGO_DATABASE"),
            instapush_appid=crawler.settings.get("INSTAPUSH_APPID", ""),
            instapush_secret=crawler.settings.get("INSTAPUSH_SECRET", "")
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        if self.instapush_app:
            self.instapush_app.notify(event_name='spider_events', trackers={'event': 'starts'})

    def close_spider(self, spider):
        self.client.close()
        if self.instapush_app:
            self.instapush_app.notify(event_name='spider_events', trackers={'event': 'stops'})

    def process_item(self, item, spider):
        self.db[self.collection_name].insert_one(dict(item))
        return item
