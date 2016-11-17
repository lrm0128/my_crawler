#!/usr/bin/env python
# coding=utf-8


import scrapy
import ConfigParser
from xiaoqu_url.mysql_connect.mysql_connect import MySQLConn
from xiaoqu_url.items import XiaoquDetailItem
from xiaoqu_url.log_package.log_file import logs


class CrawlXiaoQuDetail(scrapy.Spider):
    name = 'xiaoqu_lianjia_detail'
    start_urls = (
        'www.baidu.com',
    )

    def __init__(self, spider_name, district=None):
        super(CrawlXiaoQuDetail, self).__init__()
        self.spider_name = spider_name
        self.config = ConfigParser.ConfigParser()
        self.config.read('./xiaoqu_url/config_package/xiaoqu_detail.ini')
        self.item = XiaoquDetailItem()
        # tag就是数据库中的id项，用于完成任务update的时候用
        self.tag = None
        self.district = district
        self.bizcircle = None

    def start_requests(self):
        """
        从数据库中取出需要的字段，并用取出的url生成request,获得response
        :return:
        """
        mysql_conn = MySQLConn()
        city = self.config.get(self.spider_name, 'city')
        if self.district:
            sql = """
                    select url, id, district, bizcircle from url_xiaoqu_all_t where city="%s" and district='%s' and taskstatus=0;
                  """ % (city, self.district)
        else:
            sql = """select url, id, district, bizcircle from url_xiaoqu_all_t where city="%s" and taskstatus=0;""" % city
        print 'sql__--: ', sql
        data = mysql_conn.select_data(sql)
        for url_tuple in data:
            self.tag = url_tuple[1]
            self.district = url_tuple[2]
            self.bizcircle = url_tuple[3]
            logs.debug('url: %s' % url_tuple[0])
            if url_tuple[0].startswith('http'):
                yield self.make_requests_from_url(url_tuple[0])
            else:
                logs.debug('bad url: %s' % url_tuple[0])

    def parse(self, response):
        """
        在打开的详情页面获得想要的字段
        :param response:
        :return:
        """
        self.item['building_area'] = self.config.get(self.spider_name, 'building_area')
        self.item['occupy_area'] = self.config.get(self.spider_name, 'occupy_area')
        self.item['house_num'] = response.xpath(self.config.get(self.spider_name, 'house_num_xpath')).extract_first()
        self.item['volume_rate'] = self.config.get(self.spider_name, 'volume_rate')
        self.item['green_rate'] = self.config.get(self.spider_name, 'green_rate')
        self.item['sale_price'] = response.xpath(self.config.get(self.spider_name, 'sale_price_xpath')).extract_first()
        self.item['develop_company'] = response.xpath(self.config.get(self.spider_name, 'develop_company_xpath')).extract_first()
        self.item['property_fee'] = response.xpath(self.config.get(self.spider_name, 'property_fee_xpath')).extract_first()
        self.item['address'] = response.xpath(self.config.get(self.spider_name, 'address_xpath')).extract_first()
        self.item['building_year'] = response.xpath(self.config.get(self.spider_name, 'building_year_xpath')).extract_first()

        self.item['building_type'] = response.xpath(self.config.get(self.spider_name, 'building_type_xpath')).extract_first()
        self.item['name'] = response.xpath(self.config.get(self.spider_name, 'name_xpath')).extract_first()
        self.item['idx'] = response.xpath(self.config.get(self.spider_name, 'idx_xpath')).extract_first()
        self.item['url'] = response.url
        self.item['entry_chengjiao'] = response.xpath(self.config.get(self.spider_name, 'entry_chengjiao_xpath')).extract_first()
        self.item['entry_rent'] = response.xpath(self.config.get(self.spider_name, 'entry_rent_xpath')).extract_first()
        self.item['entry_sale'] = response.xpath(self.config.get(self.spider_name, 'entry_sale_xpath')).extract_first()
        self.item['property_company'] = response.xpath(self.config.get(self.spider_name, 'property_company_xpath')).extract_first()
        self.item['poi'] = response.xpath(self.config.get(self.spider_name, 'posi_xpath')).extract_first()
        self.item['building_num'] = response.xpath(self.config.get(self.spider_name, 'building_num_xpath')).extract_first()
        self.item['district'] = self.district
        self.item['bizcircle'] = self.bizcircle
        self.item['rent_price'] = self.config.get(self.spider_name, 'rent_price')
        self.item['city'] = self.config.get(self.spider_name, 'city')
        self.item['province'] = self.config.get(self.spider_name, 'province')
        self.item['datatype'] = self.config.get(self.spider_name, 'datatype')
        self.item['pics'] = self.config.get(self.spider_name, 'pics')
        self.item['sale_num'] = self.config.get(self.spider_name, 'sale_num')
        self.item['rent_num'] = self.config.get(self.spider_name, 'rent_num')
        self.item['house_type'] = self.config.get(self.spider_name, 'house_type')
        yield self.item
