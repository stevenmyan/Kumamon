# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.contrib.pipeline.images import ImagesPipeline
from scrapy.exceptions import DropItem
from scrapy import Request


class AppstorePipeline(object):
    def __init__(self):
        self.file = open('appstore.dat', 'wb')

    def process_item(self, item, spider):
        val = "{0}\t{1}\t{2}\n{3}\n\n".format(item['appid'], item['title'], item['intro'], item['recommended'])
        self.file.write(val)
        return item # must return (or drop) the item at the end of each pipeline, this item will be used in subsequent item pipeline


class AppstoreImagesPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        image_url = item['image_url']
        yield Request(image_url)

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        item['image_paths'] = image_paths
        return item