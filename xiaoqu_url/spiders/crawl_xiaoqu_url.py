#!/usr/bin/env python
# coding=utf-8

import scrapy
import ConfigParser
from xiaoqu_url.items import XiaoquUrlItem
from xiaoqu_url.log_package.log_file import logs


class CrawlXiaoQuSpider(scrapy.Spider):
    name = 'xiaoqu_little'
    start_urls = (
        'just for look~',
    )

    def __init__(self, spider_name):
        super(CrawlXiaoQuSpider, self).__init__()
        self.spider_name = spider_name
        self.config = ConfigParser.ConfigParser()
        self.config.read('./xiaoqu_url/config_package/xiaoqu_cfg.ini')
        self.start_urls = (
            self.config.get(self.spider_name, 'start_url'),
        )

    def parse(self, response):
        area_url_part = response.xpath('//div[@id="houselist_B03_02"]/div[1]/a/@href').extract()[1:]
        for area_url in area_url_part:
            area_url_full = response.urljoin(area_url)
            logs.debug('area_url_full: %s' % area_url_full)
            yield scrapy.Request(area_url_full, callback=self.get_page_num)

    def get_page_num(self, response, times=1):
        all_xiaoqu_num = response.xpath('//b[@class="findplotNum"]/text()').extract_first()
        xiaoqu_num_per_page = len(response.xpath('//div[@class="list rel"]'))
        logs.debug('all_xiaoqu_num: %s' % all_xiaoqu_num)
        logs.debug('xiaoqu_num_per_page: %s' % xiaoqu_num_per_page)
        logs.debug('times: %s' % times)
        if not xiaoqu_num_per_page:
            if times == 1:
                yield scrapy.Request(response.url,
                    callback=lambda response=response, times=times+1: self.get_page_num(response, times), dont_filter=True)
            return

        page_num = int(all_xiaoqu_num) / xiaoqu_num_per_page
        yushu = int(all_xiaoqu_num) % xiaoqu_num_per_page
        if yushu:
            page_num += 1
        logs.debug('page_num: %s' % page_num)
        for i in range(1, page_num+1):
            next_page = response.url[:-6] + str(i) + '_0_0/'
            logs.debug('next_page: %s' % next_page)
            yield scrapy.Request(next_page, self.get_xiaoqu_url, dont_filter=True)

    def get_xiaoqu_url(self, response, times=1):
        item = XiaoquUrlItem()
        xiaoqu_list = response.xpath('//div[@class="list rel"]')
        xiaoqu_list_length = len(xiaoqu_list)
        logs.debug("xiaoqu_list: %s" % xiaoqu_list_length)
        logs.debug("times: %s" % times)
        if not xiaoqu_list:
            if times == 1:
                yield scrapy.Request(response.url,
                callback=lambda responses=response, time=times+1: self.get_xiaoqu_url(responses, time), dont_filter=True)
            return
        elif xiaoqu_list_length != 20:
            if times == 1:
                logs.debug("times bubu: %s" % times)
                yield scrapy.Request(response.url,
                callback=lambda responses=response, time=times + 1: self.get_xiaoqu_url(responses, time), dont_filter=True)
                return

        for xiaoqu in xiaoqu_list:
            item['provice'] = self.config.get(self.spider_name, 'provice')
            item['city'] = self.config.get(self.spider_name, 'city')
            item['site'] = self.config.get(self.spider_name, 'site')
            item['Taskstatus'] = self.config.get(self.spider_name, 'Taskstatus')
            item['district'] = response.xpath('//div[@class="finder"]/a/text()').extract()[0]
            item['bizcircle'] = '' # response.xpath('//div[@class="finder"]/a/text()').extract()[1]
            item['name'] = xiaoqu.xpath('dl/dd/p/a/text()').extract_first()
            item['url'] = xiaoqu.xpath('dl/dd/p/a/@href').extract_first()
            yield item

