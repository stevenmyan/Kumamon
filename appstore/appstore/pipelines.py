# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.contrib.pipeline.images import ImagesPipeline
from scrapy.exceptions import DropItem
from scrapy import Request
import pymongo


class AppstoreWritePipeline(object):
    def __init__(self):
        self.file = open('appstore.dat', 'wb')

    def process_item(self, item, spider):
        val = "{0}\t{1}\t{2}\n{3}\n\n".format(item['appid'], item['title'], item['intro'], item['recommends'])
        self.file.write(val)
        return item  # must return (or drop) the item at the end of each pipeline, this item will be used in subsequent item pipeline


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


class AppstoreMongodbPipeline(object):
    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        """
        return an instance of this pipeline
        crawler.settings --> settings.py
        get mongo_uri & mongo_database from settings.py
        :param crawler:
        :return: crawler instance
        """
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
        """
        process data here before loading to mongodb
        :param item:
        :param spider:
        :return: item
        """
        collection_name = item.__class__.__name__  # use itemName as the collectionName
        #self.db[collection_name].remove({}) # clean this collection when new crawling starts
        self.db[collection_name].insert(dict(item))
        return item
