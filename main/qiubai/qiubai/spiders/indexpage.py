__author__ = 'jing'

import scrapy
# uncomment below to fix issue of "Scrapy gives URLError: <urlopen error timed out>"
# from scrapy import optional_features
# optional_features.remove('boto')


class QuibaiSpider(scrapy.Spider):
    name = "qiubai"
    start_urls = [
        "http://www.qiushibaike.com"
    ]

    def parse(self, response):
        print response.xpath('//div[@class="content"]').extract()