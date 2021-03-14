# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class SinaTopSummaryItem(scrapy.Item):
    ranking = scrapy.Field()
    summary = scrapy.Field()
    last_update = scrapy.Field(serializer=str)


class SpoonItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass
