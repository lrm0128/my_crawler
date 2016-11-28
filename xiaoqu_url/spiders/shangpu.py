#!/usr/bin/env python
# coding=utf-8


import scrapy


class CrawlXiaoQuDetail(scrapy.Spider):
    name = 'shangpu'
    start_urls = (
        'http://bj.sp.anjuke.com/shou/p1/',
    )

    def parse(self, response):
        shangpu_list = response.xpath('//div[@class="list-content"]/div[@class="list-item"]')
        for shangpu in shangpu_list:
            detail_url = shangpu.xpath('@link').extract_first()
            print "detail_url : %s " % detail_url
            self.save(detail_url)
        next_page = response.xpath('//a[@class="aNxt"]/@href').extract_first()
        if not next_page:
            print "程序炸了"
        else:
            yield scrapy.Request(next_page, callback=self.parse)

    def save(self, data):
        f = file('./shangpu_result.txt', 'a')
        f.write(data + '\r\n')
        f.close()

