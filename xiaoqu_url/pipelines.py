# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import ConfigParser
import hashlib
import codecs
import json
import socket
import fcntl
import struct
import datetime
from xiaoqu_url.log_package.log_file import logs
from xiaoqu_url.mysql_connect.mysql_connect import MySQLConn


def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,
        struct.pack('256s', ifname[:15])
    )[20:24])


def update_to_mysql(tag):
    sql = """update url_xiaoqu_all_t set taskstatus=1 where id='%s';""" % tag
    logs.debug('sql: %s' % sql)
    sql_conn = MySQLConn()
    sql_conn.update_to_table(sql)


class XiaoquUrlPipeline(object):

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
              values ('%s', '%s', '%s', '%s', '%s', '%s','%s', '%s', %s);""" \
              % (id, item['name'], item['provice'],item['city'],item['district'],item['bizcircle'],item['url'],
              item['site'], item['Taskstatus'])

        print "sql: ", sql
        sql_conn.inser_data(sql)

    def process_item(self, item, spider):
        if spider.name == 'xiaoqu_little':
            config = ConfigParser.ConfigParser()
            config.read('./xiaoqu_url/config_package/xiaoqu_cfg.ini')
            item = dict(item)
            f1 = codecs.open('./%s' % config.get(spider.spider_name, 'json_file'), mode='a')
            json_data = json.dumps(item, ensure_ascii=False)
            f1.write(json_data + '\r\n')
            self.save_to_mysql(item)
            return item
        elif spider.name == 'xiaoqu_detail':
            config = ConfigParser.ConfigParser()
            config.read('./xiaoqu_url/config_package/xiaoqu_detail.ini')
            ip = get_ip_address('eth0')
            item = dict(item)
            f1 = codecs.open('./%s.%s.%s' % (ip, config.get(spider.spider_name, 'json_file'),
                                             datetime.datetime.now().strftime('%Y%m%d')),
                             mode='a'
                             )
            item_json = json.dumps(item, ensure_ascii=False)
            f1.write(item_json + '\r\n')
            f1.close()
            update_to_mysql(spider.tag)
            return item
