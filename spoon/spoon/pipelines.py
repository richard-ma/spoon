# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

import pymongo
from scrapy.exceptions import DropItem


class SinaTopSummaryPipeline:
    COLLECTION_NAME = 'top_summary'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.client = None
        self.db = None

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        if item.get('summary'):
            if item.get('ranking') is None:
                item['ranking'] = 0

            self.db[self.COLLECTION_NAME].insert_one(ItemAdapter(item).asdict())

            return item
        else:
            raise DropItem("Summary is None")


class SpoonPipeline:
    def process_item(self, item, spider):
        return item
