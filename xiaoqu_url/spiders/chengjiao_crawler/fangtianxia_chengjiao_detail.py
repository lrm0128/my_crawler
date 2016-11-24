#!/usr/bin/env python
# coding=utf-8

import os
import scrapy
import datetime
import ConfigParser
from xiaoqu_url.mysql_connect.mysql_connect import MySQLConn
from xiaoqu_url.items import HouseDetailItems
from xiaoqu_url.log_package.log_file import logs


class HouseDetailCrawler(scrapy.Spider):
    name = "house_detail"
    start_urls = (
        'just for look heheda~~',
    )

    def __init__(self, spider_name, site):
        super(HouseDetailCrawler, self).__init__()
        self.spider_name = spider_name
        self.config = ConfigParser.ConfigParser()
        print 'i am here hehe da '
        self.config.read('./fangTX/house_detail.ini')
        self.city = self.config.get(self.spider_name, 'city')
        self.site = site

    def start_requests(self):
        msq = MySQLConn()
        sql = """
        select url from url_info_all_t where city='%s' and taskstatus='0';
        """ % self.city
        data = msq.select_info(sql)
        for url_tuple in data:
            logs.debug('is going to look: %s' % url_tuple[0])
            yield self.make_requests_from_url(url_tuple[0])

    def parse(self, response):
        print "i am in parse"
        item = HouseDetailItems()
        pause = {}
        house_detail = response.xpath('//div[@id="chengjiaoxq_B02_02"]')
        v1 = house_detail.xpath('div/p[1]/text()').extract_first()
        k1 = house_detail.xpath('div/p[1]/b/text()').extract_first()
        v2 = house_detail.xpath('div/p[2]/text()').extract_first()
        k2 = house_detail.xpath('div/p[2]/b/text()').extract_first()
        v3 = house_detail.xpath('div/p[3]/a[1]/text()').extract_first()
        k3 = house_detail.xpath('div/p[3]/b/text()').extract_first()
        keys = [k1, k2, k3]
        vals = [v1, v2, v3]
        for i in range(3):
            if keys[i]:
                pause[keys[i].encode('utf-8')] = vals[i]

        # pause = {k1.encode('utf-8'): v1, k2.encode('utf-8'): v2, k3.encode('utf-8'): v3}
        item['total_floor'] = pause.get('楼层：', '')
        item['floor'] = pause.get('楼层：', '')
        item['xiaoqu_id'] = pause.get('小区：', '')
        item['area'] = pause.get('面积：', '')
        item['house_orientation'] = house_detail.xpath('ul/li[3]/p[2]/b/text()').extract_first()
        item['total_price'] = house_detail.xpath('ul/li[1]/p[2]/b/text()').extract_first()
        item['deal_time'] = response.xpath('//div[@class="mainBoxL"]/div/h1/span/text()').extract_first()
        item['name'] = pause.get('小区：', '')
        item['idx'] = pause.get('小区：', '')
        item['house_structure'] = response.xpath('//div[@class="title title1"]/h1/text()').extract_first()
        item['unit_price'] = house_detail.xpath('ul/li[2]/p[2]/b/text()').extract_first()
        item['house_year'] = self.config.get(self.spider_name, 'house_year')
        item['provice'] = self.config.get(self.spider_name, 'provice')
        item['decorate_status'] = self.config.get(self.spider_name, 'decorate_status')
        item['site'] = self.config.get(self.spider_name, 'site')
        item['city'] = self.config.get(self.spider_name, 'city')
        item['pub_time'] = self.config.get(self.spider_name, 'pub_time')
        item['deal_status'] = self.config.getint(self.spider_name, 'deal_status')
        item['crawl_time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        item['url'] = response.url
        item['house_type'] = self.config.get(self.spider_name, 'house_type')
        item['district'] = house_detail.xpath('div/p[3]/a[2]/text()').extract_first()
        yield item
