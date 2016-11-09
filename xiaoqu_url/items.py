# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class XiaoquUrlItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    provice = scrapy.Field()
    name = scrapy.Field()
    city = scrapy.Field()
    district = scrapy.Field()
    bizcircle = scrapy.Field()
    url = scrapy.Field()
    site = scrapy.Field()
    Taskstatus = scrapy.Field()

