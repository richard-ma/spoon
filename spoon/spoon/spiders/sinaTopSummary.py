import scrapy
from datetime import datetime

from spoon.items import SinaTopSummaryItem


class SinatopsummarySpider(scrapy.Spider):
    name = 'sinaTopSummary'
    allowed_domains = ['weibo.com']
    start_urls = ['https://s.weibo.com/top/summary/']

    def parse(self, response):
        print(response.url)
        last_update = datetime.now()
        tr_list = response.xpath('//tr')
        for tr in tr_list:
            item = SinaTopSummaryItem()
            item['ranking'] = tr.xpath('./td[@class="td-02"]/span/text()').extract_first()
            item['summary'] = tr.xpath('./td[@class="td-02"]/a/text()').extract_first()
            item['link'] = response.urljoin(tr.xpath('./td[@class="td-02"]/a/@href').extract_first())
            item['last_update'] = last_update

            yield item
