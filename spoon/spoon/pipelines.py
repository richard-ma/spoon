# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

import pymongo
from scrapy.utils.project import get_project_settings
from scrapy.exceptions import DropItem


class SinaTopSummaryPipeline:
    def __init__(self):
        self.settings = get_project_settings()
        self.connection = None
        self.db = None
        self.collection = None

    def open_spider(self, spider):
        self.connection = pymongo.MongoClient(
            self.settings['MONGODB_SERVER'],
            self.settings['MONGODB_PORT']
        )
        self.db = self.connection[self.settings['MONGODB_DB']]
        self.collection = self.db[self.settings['MONGODB_COLLECTION']]

    def close_spider(self, spider):
        self.connection.close()

    def process_item(self, item, spider):
        if item.get('summary'):
            if item.get('ranking') is None:
                item['ranking'] = 0

            self.collection.insert(dict(item))

            return item
        else:
            raise DropItem("Summary is None")


class SpoonPipeline:
    def process_item(self, item, spider):
        return item
