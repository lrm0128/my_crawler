# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import ConfigParser
import hashlib
import codecs
import json
from xiaoqu_url.mysql_connect.mysql_connect import MySQLConn


class XiaoquUrlPipeline(object):

    def __init__(self):
        self.config = ConfigParser.ConfigParser()
        self.config.read('./xiaoqu_url/config_package/xiaoqu_cfg.ini')

    def transformd5(self, data):
        m = hashlib.md5()
        m.update(data)
        return m.hexdigest()

    def save_to_mysql(self, item):
        sql_conn = MySQLConn()
        data = item['city'] + item['district'] + item['name']
        print "item['city'] + item['district'] + item['name']: ", data
        id = self.transformd5(data)
        sql = """insert into url_xiaoqu_all_t
              (id, name, province, city, district, bizcircle, url, site, taskstatus)
              values ('%s', '%s', '%s', '%s', '%s', '%s','%s', '%s', '%s');""" \
              % (id, item['name'], item['provice'],item['city'],item['district'],item['bizcircle'],item['url'],
              item['site'], item['Taskstatus'])

        print "sql: ", sql
        sql_conn.inser_data(sql)

    def process_item(self, item, spider):
        item = dict(item)
        f1 = codecs.open('./%s' % self.config.get(spider.spider_name, 'json_file'), mode='a')
        json_data = json.dumps(item, ensure_ascii=False)
        f1.write(json_data + '\r\n')
        self.save_to_mysql(item)
        return item
