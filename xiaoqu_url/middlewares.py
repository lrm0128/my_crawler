#!/usr/bin/env python
# coding=utf-8

from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware


class CrawlXiaoQuMiddlewares(UserAgentMiddleware):
    agents = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:31.0) Gecko/20100101 Firefox/31.0'
    #'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36'

    def process_request(self, request, spider):
        request.headers.setdefault('User-Agent', self.agents)
