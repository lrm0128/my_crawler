# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import sys
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
reload(sys)
sys.setdefaultencoding('utf-8')


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


def my_string_process(string):
    if type(string) == "str":
        return string.strip()
    else:
        return string


class XiaoquUrlPipeline(object):

    def transformd5(self, data):
        if data:
            m = hashlib.md5()
            m.update(data)
            return m.hexdigest()
        else:
            return ' '

    def save_to_xiaoqu_mysql(self, item):
        sql_conn = MySQLConn()
        data = item['city'] + item['district'] + item['name']
        print "item['city'] + item['district'] + item['name']: ", data
        id = self.transformd5(data)
        sql = """insert into url_xiaoqu_all_t
              (id, name, province, city, district, bizcircle, url, site, taskstatus)
              values ('%s', '%s', '%s', '%s', '%s', '%s','%s', '%s', %s);""" \
              % (id, item['name'], item['provice'],item['city'],item['district'],item['bizcircle'],item['url'],
              item['site'], item['Taskstatus'])

        logs.debug("sql: %s", sql)
        sql_conn.inser_data(sql)

    def process_item(self, item, spider):
        if spider.name == 'xiaoqu_little':
            config = ConfigParser.ConfigParser()
            config.read('./xiaoqu_url/config_package/xiaoqu_cfg.ini')
            item = dict(item)
            f1 = codecs.open('./%s' % config.get(spider.spider_name, 'json_file'), mode='a')
            json_data = json.dumps(item, ensure_ascii=False)
            f1.write(json_data + '\r\n')
            self.save_to_xiaoqu_mysql(item)
            return item
        elif spider.name == 'xiaoqu_fang_detail':
            config = ConfigParser.ConfigParser()
            config.read('./xiaoqu_url/config_package/xiaoqu_detail.ini')
            ip = get_ip_address('eth0')
            item = dict(item)
            f1 = codecs.open('./out_put/%s.%s.%s' % (ip, config.get(spider.spider_name, 'json_file'),
                                             datetime.datetime.now().strftime('%Y%m%d')),
                             mode='a'
                             )
            item_json = json.dumps(item, ensure_ascii=False)
            f1.write(item_json + '\r\n')
            f1.close()
            update_to_mysql(spider.tag)
            return item
        elif spider.name == 'xiaoqu_lianjia_detail':
            config = ConfigParser.ConfigParser()
            config.read('./xiaoqu_url/config_package/xiaoqu_detail.ini')
            ip = get_ip_address('eth0')
            item = dict(item)
            for key in item:
                if not item[key]:
                    item[key] = 'na'
                else:
                    processed_val = my_string_process(item[key])
                    item[key] = processed_val
            f1 = codecs.open('./out_put/%s.%s.%s' % (ip, config.get(spider.spider_name, 'json_file'),
                                             datetime.datetime.now().strftime('%Y%m%d')), mode='a'
                             )
            item_json = json.dumps(item, ensure_ascii=False)
            f1.write(item_json + '\r\n')
            f1.close()
            update_to_mysql(spider.tag)
            return item
        elif spider.name in ["chengjiao_url", "sh_chengjiao_url"]:
            config = ConfigParser.ConfigParser()
            config.read('./xiaoqu_url/config_package/chengjiao_url_cfg.ini')
            data = dict(item)
            for key in item:
                if not item[key]:
                    item[key] = 'na'
                else:
                    processed_val = my_string_process(item[key])
                    item[key] = processed_val
            if not data['name']:
                return "无效url"
            url_md5 = self.transformd5(data['url'])
            sql = """
            insert into url_info_all_t (name, province, city, district, bizcircle, url, datatype, taskstatus, url_md5)
            values ('%s', '%s', '%s', '%s', '%s', '%s', '%s', %s, '%s');
            """ % (data['name'], data['provice'], data['city'], data['district'], data['bizcircle'], data['url'],
                   data['datatype'], data['Taskstatus'], url_md5)
            logs.debug("sql: %s", sql)
            f1 = codecs.open('./out_put/%s' % config.get(spider.spider_name, 'json_file'), mode='a')
            json_data = json.dumps(data, ensure_ascii=False)
            f1.write(json_data + '\r\n')
            f1.close()
            sql_conn = MySQLConn()
            # sql_conn.inser_data(sql)
            return item
        elif spider.name == "chengjiao_lianjia_detail" or spider.name == "sh_chengjiao_lianjia_detail":
            config = ConfigParser.ConfigParser()
            config.read('./xiaoqu_url/config_package/chengjiao_detail_cfg.ini')
            ip = get_ip_address('eth0')
            item = dict(item)
            for key in item:
                if not item[key]:
                    item[key] = 'na'
                else:
                    processed_val = my_string_process(item[key])
                    item[key] = processed_val
            f1 = codecs.open('./out_put/%s.%s.%s' % (ip, config.get(spider.spider_name, 'json_file'),
                        datetime.datetime.now().strftime('%Y%m%d')), mode='a'
                             )
            item_json = json.dumps(item, ensure_ascii=False)
            f1.write(item_json + '\r\n')
            f1.close()
            sql = """
            update url_xiaoqu_all_t set taskstatus=1 where url_md5='%s'
            """ % spider.tag
            logs.debug("sql: %s" % sql)
            sql_conn = MySQLConn()
            sql_conn.update_to_table(sql)
            return item
        elif spider.name == "ershoufang_url":
            config = ConfigParser.ConfigParser()
            config.read('./xiaoqu_url/config_package/sale_url_cfg.ini')
            data = dict(item)
            for key in item:
                if not item[key]:
                    item[key] = 'na'
                else:
                    processed_val = my_string_process(item[key])
                    item[key] = processed_val
            if not data['name']:
                return "无效url"
            url_md5 = self.transformd5(data['url'])
            sql = """
                        insert into url_info_all_t (name, province, city, district, bizcircle, url, datatype, taskstatus, url_md5)
                        values ('%s', '%s', '%s', '%s', '%s', '%s', '%s', %s, '%s');
                        """ % (
            data['name'], data['provice'], data['city'], data['district'], data['bizcircle'], data['url'],
            data['datatype'], data['Taskstatus'], url_md5)
            logs.debug("sql: %s", sql)
            f1 = codecs.open('./out_put/%s' % config.get(spider.spider_name, 'json_file'), mode='a')
            json_data = json.dumps(data, ensure_ascii=False)
            f1.write(json_data + '\r\n')
            f1.close()
            sql_conn = MySQLConn()
            sql_conn.inser_data(sql)
            return item
