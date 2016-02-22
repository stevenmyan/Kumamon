# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class AppstoreItem(Item):
    # define the fields for your item here like:
    title = Field()
    url = Field()
    appid = Field()
    intro = Field()
    recommended = Field()

    # image
    image_url = Field()
    image_paths = Field()
