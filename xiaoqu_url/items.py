# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class HubItem(scrapy.Item):
    provice = scrapy.Field()
    name = scrapy.Field()
    city = scrapy.Field()
    district = scrapy.Field()
    bizcircle = scrapy.Field()
    url = scrapy.Field()
    datatype = scrapy.Field()
    Taskstatus = scrapy.Field()


class HouseDetailItems(scrapy.Item):
    province = scrapy.Field()
    decorate_status = scrapy.Field()
    total_floor = scrapy.Field()
    site = scrapy.Field()
    house_orientation = scrapy.Field()
    total_price = scrapy.Field()
    xiaoqu_id = scrapy.Field()
    house_type = scrapy.Field()
    deal_time = scrapy.Field()
    city = scrapy.Field()
    pub_time = scrapy.Field()
    deal_status = scrapy.Field()
    name = scrapy.Field()
    idx = scrapy.Field()
    area = scrapy.Field()
    datatype = scrapy.Field()
    house_structure = scrapy.Field()
    floor = scrapy.Field()
    unit_price = scrapy.Field()
    url = scrapy.Field()
    house_year = scrapy.Field()
    crawl_time = scrapy.Field()
    district = scrapy.Field()


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


class XiaoquDetailItem(scrapy.Item):
    building_area = scrapy.Field()
    occupy_area = scrapy.Field()
    poi = scrapy.Field()
    house_num = scrapy.Field()
    city = scrapy.Field()
    district = scrapy.Field()
    volume_rate = scrapy.Field()
    green_rate = scrapy.Field()
    sale_price = scrapy.Field()
    bizcircle = scrapy.Field()
    develop_company = scrapy.Field()
    province = scrapy.Field()
    property_fee = scrapy.Field()
    rent_num = scrapy.Field()
    datatype = scrapy.Field()
    building_num = scrapy.Field()
    entry_chengjiao = scrapy.Field()
    address = scrapy.Field()
    building_year = scrapy.Field()
    name = scrapy.Field()
    idx = scrapy.Field()
    url = scrapy.Field()
    pics = scrapy.Field()
    entry_rent = scrapy.Field()
    rent_price = scrapy.Field()
    building_type = scrapy.Field()
    property_company = scrapy.Field()
    entry_sale = scrapy.Field()
    house_type = scrapy.Field()
    sale_num = scrapy.Field()
