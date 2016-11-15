#!/usr/bin/env python
# coding=utf-8

import scrapy
import ConfigParser
from xiaoqu_url.mysql_connect.mysql_connect import MySQLConn
from xiaoqu_url.items import XiaoquDetailItem
from xiaoqu_url.log_package.log_file import logs


class CrawlXiaoQuDetail(scrapy.Spider):
    name = 'xiaoqu_fang_detail'
    start_urls = (
        'www.baidu.com',
    )

    def __init__(self, spider_name):
        super(CrawlXiaoQuDetail, self).__init__()
        self.spider_name = spider_name
        self.config = ConfigParser.ConfigParser()
        self.config.read('./xiaoqu_url/config_package/xiaoqu_detail.ini')
        self.item = XiaoquDetailItem()
        self.tag = None

    def start_requests(self):
        """
        查找数据库获得指定的URL并过滤部分不可用的URL
        :return:
        """
        mysql_conn = MySQLConn()
        city = self.config.get(self.spider_name, 'city')
        sql = """select url, id from url_xiaoqu_all_t where city="%s" and taskstatus=0;""" % city
        data = mysql_conn.select_data(sql)
        for url_tuple in data:
            self.tag = url_tuple[1]
            logs.debug('url: %s' % url_tuple[0])
            logs.debug('self.tag: %s' % url_tuple[1])
            if url_tuple[0].startswith('http'):
                yield self.make_requests_from_url(url_tuple[0])
            else:
                logs.debug('bad url: %s' % url_tuple[0])

    def parse(self, response):
        """
        获得详情页的url
        :param response:
        :return:
        """
        logs.debug('response.url: %s' % response.url)
        raw_url = response.url
        if raw_url.endswith('esf/'):
            raw_url_list = raw_url.split('/')
            raw_url_list[-2] = 'xiangqing'
            detail_url = '/'.join(raw_url_list)
            logs.debug('detail_url: %s' % detail_url)
        else:
            detail_url = raw_url+'xiangqing/'
        yield scrapy.Request(detail_url, callback=self.crawl_items)

    def crawl_items(self, response):
        """
        抓取需要的字段
        :param response:
        :return:
        """
        result_dict = {}
        logs.debug('is going to check: %s' % response.url)
        basic_info = response.xpath('//dl[@class=" clearfix mr30"]')
        if basic_info:
            basic_info = basic_info[0]
        else:
            return
        basic_info_items = basic_info.xpath('dd')
        # 由于房天下的数据字段数目不一致， 位置也不固定，所以先全部存储下来，放在字典中
        # 根据键值选取需要的字段
        for line in basic_info_items:
            key = line.xpath('strong/text()').extract_first()
            val = line.xpath('text()').extract_first()
            logs.debug('key: %s' % key)
            logs.debug('val: %s' % val)
            if key:
                result_dict[key.encode('utf-8')] = val
        logs.debug('result_dict: %s' % result_dict)
        self.item['building_area'] = result_dict.get('建筑面积：', '')
        self.item['occupy_area'] = result_dict.get('占地面积：', '')
        self.item['house_num'] = result_dict.get('总 户 数：', '')
        self.item['volume_rate'] = result_dict.get('容 积 率：', '')
        self.item['green_rate'] = result_dict.get('绿 化 率：', '')
        self.item['sale_price'] = response.xpath('//div[@class="box detaiLtop mt20 clearfix"]/dl[1]/dd/span/text()').extract_first()
        self.item['develop_company'] = result_dict.get('开 发 商：', '')
        self.item['property_fee'] = result_dict.get('物 业 费：', '')
        self.item['address'] = result_dict.get('小区地址：', '')
        self.item['building_year'] = result_dict.get('竣工时间：', '')
        self.item['building_type'] = result_dict.get('建筑类别：', '')
        self.item['name'] = response.xpath('//a[@class="tt"]/text()').extract_first()
        self.item['idx'] = response.xpath('//a[@class="tt"]/text()').extract_first()
        self.item['url'] = response.url
        self.item['entry_chengjiao'] = response.url.replace('xiangqing', 'chengjiao')
        self.item['entry_rent'] = response.url.replace('xiangqing', 'chuzu')
        self.item['entry_sale'] = response.url.replace('xiangqing', 'chushou')
        self.item['property_company'] = self.config.get(self.spider_name, 'property_company')
        self.item['posi'] = self.config.get(self.spider_name, 'posi')
        yield scrapy.Request(response.url.replace('xiangqing', 'chuzu'), callback=self.rent_info)

    def rent_info(self, response):
        logs.debug('rent_xiaoqu_url: %s' % response.url)
        self.item['district'] = response.xpath('//div[@class="rentListwrap fangListwrap"]/div[1]/dl/dd/p[3]/a[1]/text()').extract_first()
        self.item['bizcircle'] = response.xpath('//div[@class="rentListwrap fangListwrap"]/div[1]/dl/dd/p[3]/a[2]/text()').extract_first()
        self.item['rent_price'] = response.xpath('//div[@class="esfHousedetail"]/p[2]/span[1]/b/text()').extract_first()
        self.item['city'] = self.config.get(self.spider_name, 'city')
        self.item['province'] = self.config.get(self.spider_name, 'province')
        self.item['datatype'] = self.config.get(self.spider_name, 'datatype')
        self.item['building_num'] = self.config.get(self.spider_name, 'building_num')
        self.item['pics'] = self.config.get(self.spider_name, 'pics')
        self.item['property_company'] = self.config.get(self.spider_name, 'property_company')
        self.item['sale_num'] = self.config.get(self.spider_name, 'sale_num')
        self.item['rent_num'] = self.config.get(self.spider_name, 'rent_num')
        self.item['house_type'] = self.config.get(self.spider_name, 'house_type')
        yield self.item
