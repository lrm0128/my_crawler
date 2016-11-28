#!/usr/bin/env python
# coding=utf-8


import scrapy
import datetime
import ConfigParser
from xiaoqu_url.mysql_connect.mysql_connect import MySQLConn
from xiaoqu_url.items import HouseDetailItems
from xiaoqu_url.log_package.log_file import logs


class CrawlXiaoQuDetail(scrapy.Spider):
    name = 'ershoufang_detail'
    start_urls = (
        'www.baidu.com',
    )

    def __init__(self, spider_name, district=None):
        super(CrawlXiaoQuDetail, self).__init__()
        self.spider_name = spider_name
        self.config = ConfigParser.ConfigParser()
        self.config.read('./xiaoqu_url/config_package/sale_detail_cfg.ini')
        self.item = HouseDetailItems()
        # tag就是数据库中的id项，用于完成任务update的时候用
        # self.tag = None
        # self.district = district

    def start_requests(self):
        """
        从数据库中取出需要的字段，并用取出的url生成request,获得response
        :return:
        """
        mysql_conn = MySQLConn()
        city = self.config.get(self.spider_name, 'city')
        if self.district:
            sql = """
                    select url, url_md5, district from url_info_all_t where city="%s" and district='%s' and taskstatus=0 and datatype="sale";
                  """ % (city, self.district)
        else:
            sql = """
                select url, url_md5, district from url_info_all_t where city="%s" and taskstatus=0 and datatype="sale";
                  """ % city
        print 'sql__--: ', sql
        data = mysql_conn.select_data(sql)
        for url_tuple in data:
            # self.tag = url_tuple[1]
            # self.district = url_tuple[2]
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
        mysql_conn = MySQLConn()
        sql = """
            select district from url_info_all_t where url="%s";
        """ % response.url
        data_tuple = mysql_conn.select_data(sql)
        base_info = response.xpath(self.config.get(self.spider_name, "base_info"))
        self.config.get(self.spider_name, "base_info")
        self.item["province"] = self.config.get(self.spider_name, "province")
        self.item["decorate_status"] = base_info.xpath(self.config.get(self.spider_name, "decorate_status_xpath")).re_first('\S+')
        self.item["total_floor"] = base_info.xpath(self.config.get(self.spider_name, "total_floor")).re_first('\S+')
        self.item["site"] = self.config.get(self.spider_name, "site")
        self.item["house_orientation"] = base_info.xpath(self.config.get(self.spider_name, "house_orientation")).re_first('\S+')
        self.item["total_price"] = base_info.xpath(self.config.get(self.spider_name, "total_price")).re_first('\S+')
        self.item["xiaoqu_id"] = response.xpath(self.config.get(self.spider_name, "xiaoqu_id")).re_first('\S+')
        self.item["house_type"] = self.config.get(self.spider_name, "house_type")
        self.item["deal_time"] = response.xpath(self.config.get(self.spider_name, "deal_time")).re_first('\S+')
        self.item["city"] = self.config.get(self.spider_name, "city")
        self.item["pub_time"] = self.config.get(self.spider_name, "pub_time")
        self.item["deal_status"] = self.config.getint(self.spider_name, "deal_status")
        self.item["name"] = response.xpath(self.config.get(self.spider_name, "name")).re_first('\S+')
        self.item["idx"] = response.xpath(self.config.get(self.spider_name, "idx")).re_first('\S+')
        self.item["area"] = response.xpath(self.config.get(self.spider_name, "area")).extract_first()
        if self.spider_name in ['sh_ershoufang_lianjia_house', 'su_ershoufang_lianjia_house']:
            house_structure_elements = response.xpath(self.config.get(self.spider_name, "house_structure")).re('(\d)<.*?>(\w)')
            self.item["house_structure"] = ''.join(house_structure_elements)
        else:
            self.item["house_structure"] = response.xpath(self.config.get(self.spider_name, "house_structure")).extract_first()
        self.item["floor"] = base_info.xpath(self.config.get(self.spider_name, "floor")).re_first('\S+')
        self.item["unit_price"] = base_info.xpath(self.config.get(self.spider_name, "unit_price")).re_first('\S+')
        self.item["url"] = response.url
        self.item["house_year"] = base_info.xpath(self.config.get(self.spider_name, "house_year")).re_first('\S+')
        self.item["crawl_time"] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.item["district"] = data_tuple[0][0]
        print "heheda", self.item
        yield self.item
