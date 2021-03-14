import scrapy

from spoon.items import SinaTopSummaryItem


class SinatopsummarySpider(scrapy.Spider):
    name = 'sinaTopSummary'
    allowed_domains = ['weibo.com']
    start_urls = ['https://s.weibo.com/top/summary/']

    def parse(self, response):
        tr_list = response.xpath('//tr')
        for tr in tr_list:
            item = SinaTopSummaryItem()
            item['ranking'] = tr.xpath('./td[contains(@class, "ranktop")]/text()').extract_first()
            item['summary'] = tr.xpath('./td[@class="td-02"]/a/text()').extract_first()

            yield item
