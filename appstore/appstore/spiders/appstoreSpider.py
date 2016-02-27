# coding=utf-8
__author__ = 'jing'

from scrapy.spider import BaseSpider
from scrapy import Request
import re
from scrapy.selector import Selector, HtmlXPathSelector
from appstore.items import AppstoreItem

# uncomment below to fix issue of "Scrapy gives URLError: <urlopen error timed out>"
from scrapy import optional_features
optional_features.remove('boto')


class HuaweiSpider(BaseSpider):
    name = "appstore"

    allowed_domains = ["huawei.com"]

    start_urls = [
        "http://appstore.huawei.com/more/all"
    ]

    def parse(self, response):
        page = Selector(response)
        divs = page.xpath('//div[@class="list-game-app dotline-btn nofloat"]')

        #print to debug
        print len(divs)
        print divs

        for div in divs:
            item = AppstoreItem()

            # image
            image_url = div.xpath('.//div[@class="game-info-ico"]//img[@class="app-ico"]/@lazyload').extract()[0] #这里lazyload属性在view page source里面可以看见
            item["image_url"] = image_url


            # stats
            info = div.xpath('.//div[@class="game-info  whole"]')
            item["title"] = info.xpath('./h4[@class="title"]/a/text()').extract_first().encode('utf-8')
            item["url"] = info.xpath('./h4[@class="title"]/a/@href').extract_first()
            item["appid"] = re.match(r'http://.*/(.*)', item["url"]).group(1)  #appid is extracted from url
            item["intro"] = info.xpath('.//p[@class="content"]/text()').extract_first().encode('utf-8')  #这里p标签不是div变量的子标签,是孙子标签

            # child page for more details
            # pass existing item to child page via attr meta
            href = div.xpath('.//div[@class="game-info  whole"]//a/@href').extract_first()
            req = Request(href, callback=self.parse_detail_page, meta={'item': item})
            yield req

    def parse_detail_page(self, response):
        item = response.meta["item"]

        divs = response.xpath('//div[@class="app-sweatch  nofloat"]')
        recommended = []
        for div in divs:
            rank = div.xpath('.//em[@class="num-red"]/text()').extract_first()
            name = div.xpath('.//p[@class="name"]/a/text()').extract_first().encode('utf-8')
            url = div.xpath('.//p[@class="name"]/a/@href').extract_first()
            recommended_appid = re.match(r'http://.*/(.*)', url).group(1)
            recommended.append({'name-red': name, 'rank-red': rank, 'appid-red':recommended_appid})

        item["recommended"] = recommended
        yield item

