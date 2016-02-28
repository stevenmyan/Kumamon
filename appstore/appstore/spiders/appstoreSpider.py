# coding=utf-8
__author__ = 'jing'

from scrapy.spider import BaseSpider
from scrapy import Request
import scrapy
import re
from scrapy.selector import Selector
from appstore.items import AppstoreItem

# fix issue of "Scrapy gives URLError: <urlopen error timed out>"
from scrapy import optional_features
optional_features.remove('boto')


class HuaweiSpider(BaseSpider):
    name = "appstore"

    allowed_domains = ["huawei.com"]

    start_urls = [
        "http://appstore.huawei.com/more/all"
    ]

    # render since the start url
    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, self.parse, meta={
                'splash': {
                    'endpoint': 'render.html',
                    'args': {'wait': 0.5}
                }
            })


    def parse(self, response):
        """
        response.body is a result of render.html call; it contains HTML processed by a browser.
        here we parse the html
        :param response:
        :return: request to detail page & request to next page if exists
        """
        page = Selector(response)
        divs = page.xpath('//div[@class="list-game-app dotline-btn nofloat"]')
        current_url = response.url
        print "num of app in current page: ", len(divs)
        print "current url: ", current_url

        # parse details
        count = 0
        for div in divs:
            if count >= 2:
                break
            item = AppstoreItem()
            info = div.xpath('.//div[@class="game-info  whole"]')
            detail_url = info.xpath('./h4[@class="title"]/a/@href').extract_first()
            item["url"] = detail_url
            req = Request(detail_url, callback=self.parse_detail_page)
            req.meta["item"] = item
            count += 1
            yield req

        # next page
        page_ctrl = response.xpath('//div[@class="page-ctrl ctrl-app"]')
        isNextPageThere = page_ctrl.xpath('.//em[@class="arrow-grey-rt"]').extract()

        if isNextPageThere:
            current_page_index = int(page_ctrl.xpath('./span[not(@*)]/text()').extract_first()) # not any on specific attr "div[not(@attr)]"
            if current_page_index >= 5:
                print "let's stop here for now"
                return
            next_page_index = str(current_page_index + 1)

            next_page_url = self.start_urls[0] + "/" + next_page_index

            print "next_page_index: ", next_page_index, "next_page_url: ", next_page_url
            request = scrapy.Request(next_page_url, callback=self.parse, meta={ # render the next page
                'splash': {
                    'endpoint': 'render.html',
                    'args': {'wait': 0.5}
                },
            })
            yield request
        else:
            print "this is the end!"


    def parse_detail_page(self, response):
        """
        GET details for each app
        :param response:
        :return: item
        """
        item = response.meta["item"]

        # details about current app
        item["image_url"] = response.xpath('//ul[@class="app-info-ul nofloat"]//img[@class="app-ico"]/@lazyload').extract()[0]
        item["title"] = response.xpath('//ul[@class="app-info-ul nofloat"]//span[@class="title"]/text()').extract_first().encode('utf-8')
        item["appid"] = re.match(r'http://.*/(.*)', item["url"]).group(1)
        item["intro"] = response.xpath('//div[@class="content"]/div[@id="app_strdesc"]/text()').extract_first().encode('utf-8')

        # recommended apps
        divs = response.xpath('//div[@class="unit nofloat corner"]/div[@class="unit-main nofloat"]/div[@class="app-sweatch  nofloat"]')
        recommends = []
        for div in divs:
            rank = div.xpath('./div[@class="open nofloat"]/em/text()').extract_first()
            name = div.xpath('./div[@class="open nofloat"]/div[@class="open-info"]/p[@class="name"]/a/@title').extract()[0].encode('utf-8')
            url = div.xpath('./div[@class="open nofloat"]/div[@class="open-info"]/p[@class="name"]/a/@href').extract_first()
            rec_appid = re.match(r'http://.*/(.*)', url).group(1)
            recommends.append({'name': name, 'rank': rank, 'appid': rec_appid})

        item["recommends"] = recommends
        yield item
