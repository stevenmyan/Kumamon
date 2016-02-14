__author__ = 'jing'

import scrapy
#
# # uncomment below to fix Scrapy gives URLError: <urlopen error timed out>
# from scrapy import optional_features
# optional_features.remove('boto')


class QuibaiSpider(scrapy.Spider):
    name = "qiubai"
    start_urls = [
        "http://www.qiushibaike.com"
    ]

    def parse(self, response):
        print response.xpath('//div[@class="content"]').extract()


# DOWNLOAD_HANDLERS = {'S3':None,}
#
# # Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.103 Safari/537.36'