#!/usr/bin/env python
# coding=utf-8

import scrapy
import ConfigParser
from xiaoqu_url.items import HubItem
from xiaoqu_url.log_package.log_file import logs


class CrawlXiaoQuSpider(scrapy.Spider):
    """
    抓取URL，并保存在数据库中
    """
    name = 'ershoufang_url'
    start_urls = (
        'just for look~',
    )

    def __init__(self, spider_name):
        super(CrawlXiaoQuSpider, self).__init__()
        self.spider_name = spider_name
        self.config = ConfigParser.ConfigParser()
        self.config.read('./xiaoqu_url/config_package/sale_url_cfg.ini')
        self.start_urls = (
            self.config.get(self.spider_name, 'start_url'),
        )

    def parse(self, response):
        """
        获得行政区的url
        :param response:
        :return:
        """
        district_start = self.config.getint(self.spider_name, 'district_start')
        area_url_part = response.xpath(self.config.get(self.spider_name, 'district_xpath'))[district_start:]
        for area_url in area_url_part:
            district = area_url.xpath('text()').extract_first()
            area_url_full = response.urljoin(area_url.xpath('@href').extract_first())
            logs.debug('area_url_full: %s' % area_url_full)
            logs.debug('district: %s' % district)
            yield scrapy.Request(area_url_full,
                callback=lambda response=response, district=district: self.get_sub_area(response, district))

    def get_sub_area(self, response, district):
        """
        获得商圈的url
        :param response:
        :return:
        """
        logs.debug('district---: %s' %district)
        sub_area_start = self.config.getint(self.spider_name, 'sub_area_start')
        sub_area_url_part = response.xpath(self.config.get(self.spider_name, 'sub_area_xpath'))[sub_area_start:]
        for sub_area_url in sub_area_url_part:
            bizcircle = sub_area_url.xpath('text()').extract_first()
            sub_area_url_full = response.urljoin(sub_area_url.xpath('@href').extract_first())
            logs.debug('sub_area_url_full: %s' % sub_area_url_full)
            logs.debug('self.bizcircle: %s' % bizcircle)
            yield scrapy.Request(sub_area_url_full,
                callback=lambda response=response, bizcircle=bizcircle, district=district:
                self.get_page_num(response, district, bizcircle))

    def get_page_num(self, response, district, bizcircle, times=1):
        """
        从商圈中获取指定商圈的页面数
        注：由于房天下数据存在抖动，可能出现为空的页面，所以若出现为空的页面再访问一次，以确保能够爬取一个全量的数据
        :param response:
        :param times:
        :return:
        """
        all_ershoufang_num = response.xpath(self.config.get(self.spider_name, 'ershoufang_num_xpath')).extract_first()
        ershoufang_num_per_page = len(response.xpath(self.config.get(self.spider_name, 'ershoufang_list_xpath')))
        logs.debug('all_ershoufang_num: %s' % all_ershoufang_num)
        logs.debug('ershoufang_num_per_page: %s' % ershoufang_num_per_page)
        logs.debug('times: %s' % times)
        if not ershoufang_num_per_page:
            if times == 1:
                yield scrapy.Request(response.url,
                    callback=lambda response=response, times=times+1, district=district, bizcircle=bizcircle:
                    self.get_page_num(response, district, bizcircle, times), dont_filter=True)
            return
        page_num = int(all_ershoufang_num) / ershoufang_num_per_page
        yushu = int(all_ershoufang_num) % ershoufang_num_per_page
        if yushu:
            page_num += 1
        logs.debug('page_num: %s' % page_num)
        url_list = self.make_url_for_page(page_num, response.url)
        if url_list:
            for url in url_list:
                logs.debug('next_page: %s' % url)
                yield scrapy.Request(url, callback=lambda response=response, district=district, bizcircle=bizcircle:
                    self.get_ershoufang_url(response, district, bizcircle), dont_filter=True)

    def make_url_for_page(self, page_num, url):
        """
        制作每一页的URL，并放在列表中返回
        :param page_num:
        :param url:
        :return:
        """
        url_list = []
        if "fang" in self.spider_name:
            for i in range(1, page_num+1):
                next_page = url[:-6] + str(i) + '_0_0/'
                url_list.append(next_page)
        elif "lianjia1" in self.spider_name:
            for i in range(1, page_num+1):
                next_page = url + 'pg' + str(i) + '/'
                url_list.append(next_page)
        elif "lianjia2" in self.spider_name:
            for i in range(1, page_num+1):
                next_page = url + 'd' + str(i)
                url_list.append(next_page)
        return url_list

    def get_ershoufang_url(self, response, district, bizcircle, times=1):
        """
        在列表中依次获得指定小区的关键数据
        :param response:
        :param times:
        :return:
        """
        logs.debug("haha here the district is: %s" % district)
        logs.debug("haha here the bizcircle is: %s" % bizcircle)
        item = HubItem()
        ershoufang_list = response.xpath(self.config.get(self.spider_name, 'ershoufang_list_xpath'))
        ershoufang_list_length = len(ershoufang_list)
        logs.debug("ershoufang_list: %s" % ershoufang_list_length)
        logs.debug("times: %s" % times)
        if not ershoufang_list:
            if times == 1:
                yield scrapy.Request(response.url,
                callback=lambda responses=response, district=district, bizcircle=bizcircle, time=times+1:
                self.get_ershoufang_url(responses, district, bizcircle, time), dont_filter=True)
            return

        for ershoufang in ershoufang_list:
            print "ershoufang: ", ershoufang
            item['provice'] = self.config.get(self.spider_name, 'provice')
            item['city'] = self.config.get(self.spider_name, 'city')
            # item['site'] = self.config.get(self.spider_name, 'site')
            item['Taskstatus'] = self.config.get(self.spider_name, 'Taskstatus')
            item['district'] = district
            item['bizcircle'] = bizcircle
            item['name'] = ershoufang.xpath(self.config.get(self.spider_name, 'name_xpath')).extract_first()
            url_part = ershoufang.xpath(self.config.get(self.spider_name, 'url_xpath')).extract_first()
            item['url'] = response.urljoin(url_part)
            item['datatype'] = self.config.get(self.spider_name, 'datatype')
            logs.debug("kanghe: %s", item)
            yield item

