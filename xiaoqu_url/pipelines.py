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
    """
    获得代码运行机器的IP
    :param ifname:
    :return:
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,
        struct.pack('256s', ifname[:15])
    )[20:24])


def my_string_process(string):
    """
    对数据进行一个简单的处理，去除空字符
    :param string:
    :return:
    """
    if type(string) == "str":
        return string.strip()
    else:
        return string


class XiaoquUrlPipeline(object):
    """
    从网页上扒下来的数据在这个文件中进行存储
    分类存储的机制是根据爬虫的名字来进行区分
    """
    def transformd5(self, data):
        """
        进行简单的字符串转换为MD5编码，确保得到的数据的唯一性，避免重复
        :param data:
        :return:
        """
        if data:
            m = hashlib.md5()
            m.update(data)
            return m.hexdigest()
        else:
            return ' '

    def open_config_file(self, cfg_path):
        """
        打开配置文件，并读取
        :param cfg_path:
        :return: 配置文件的对象
        """
        config = ConfigParser.ConfigParser()
        config.read(cfg_path)
        return config

    def open_result_file(self, file_name, item):
        """
        存储网页上面的内容，以json格式存储到文件中
        :param file_name:
        :param item:
        :return:
        """
        f1 = codecs.open('./out_put/%s' % file_name, mode='a')
        json_data = json.dumps(item, ensure_ascii=False)
        f1.write(json_data + '\r\n')

    def insert_sql_execute(self, sql):
        """
        插入数据库中
        :param sql:
        :return:
        """
        mysql = MySQLConn()
        mysql.inser_data(sql)

    def update_sql_execute(self, sql):
        """
        完成任务之后更新数据库中的任务状态
        :param sql:
        :return:
        """
        mysql = MySQLConn()
        mysql.update_to_table(sql)

    def process_data(self, item):
        """
        对从网页上扒下来的数据进行初步判断是否满足要求，将空值设置为“na”
        :param item:
        :return:
        """
        for key in item:
            if not item[key]:
                item[key] = 'na'
            else:
                processed_val = my_string_process(item[key])
                item[key] = processed_val
        return item

    def process_item(self, item, spider):
        if spider.name == 'xiaoqu_url':
            item = dict(item)
            data = item['city'] + item['district'] + item['name']
            logs.debug("item['city'] + item['district'] + item['name']: %s" % data)
            ids = self.transformd5(data)
            cfg_path = './xiaoqu_url/config_package/xiaoqu_cfg_url.ini'
            sql = """insert into url_xiaoqu_all_t (id, name, province, city, district, bizcircle, url, site, taskstatus)
                values ('%s', '%s', '%s', '%s', '%s', '%s','%s', '%s', %s);""" \
                % (ids, item['name'], item['provice'],item['city'],item['district'],item['bizcircle'],item['url'],
                item['site'], item['Taskstatus'])
            config = self.open_config_file(cfg_path)
            file_name = config.get(spider.spider_name, 'json_file')
            item = self.process_data(item)
            self.open_result_file(file_name, item)
            self.insert_sql_execute(sql)
            return item
        elif spider.name in ['xiaoqu_fang_detail', 'xiaoqu_lianjia_detail']:
            cfg_path = './xiaoqu_url/config_package/xiaoqu_detail.ini'
            config = self.open_config_file(cfg_path)
            ip = get_ip_address('eth0')
            item = dict(item)
            file_name = '%s.%s.%s' % (ip, config.get(spider.spider_name, 'json_file'), datetime.datetime.now().strftime('%Y%m%d'))
            tag = item['id']
            logs.debug('tag: %s' % tag)
            logs.debug('city+district+name : %s' %(item['city']+item['district']+item['name']))
            sql = """update url_xiaoqu_all_t set taskstatus=1 where id='%s';""" % tag
            logs.debug('sql: %s' % sql)
            item.pop('id')
            self.open_result_file(file_name, item)
            self.update_sql_execute(sql)
            return item
        elif spider.name in ["chengjiao_url", "sh_chengjiao_url"]:
            cfg_path = './xiaoqu_url/config_package/chengjiao_url_cfg.ini'
            config = self.open_config_file(cfg_path)
            item = dict(item)
            if not item['name']:
                return "无效url"
            url_md5 = self.transformd5(item['url'])
            sql = """
            insert into url_info_all_t (name, province, city, district, bizcircle, url, datatype, taskstatus, url_md5)
            values ('%s', '%s', '%s', '%s', '%s', '%s', '%s', %s, '%s');
            """ % (item['name'], item['provice'], item['city'], item['district'], item['bizcircle'], item['url'],
                   item['datatype'], item['Taskstatus'], url_md5)
            logs.debug("sql: %s", sql)
            result_file = config.get(spider.spider_name, 'json_file')
            self.open_result_file(result_file, item)
            self.insert_sql_execute(sql)
            return item
        elif spider.name == "chengjiao_lianjia_detail" or spider.name == "sh_chengjiao_lianjia_detail":
            cfg_path = './xiaoqu_url/config_package/chengjiao_detail_cfg.ini'
            config = self.open_config_file(cfg_path)
            ip = get_ip_address('eth0')
            item = dict(item)
            self.process_data(item)
            result_file = '%s.%s.%s' % (ip, config.get(spider.spider_name, 'json_file'), datetime.datetime.now().strftime('%Y%m%d'))
            self.open_result_file(result_file, item)
            # url_md5 = self.transformd5(item['url'])
            sql = """
            update url_info_all_t set taskstatus=1 where url='%s'
            """ % item['url']
            logs.debug("sql: %s" % sql)
            self.update_sql_execute(sql)
            return item
        elif spider.name == "ershoufang_url":
            cfg_path = './xiaoqu_url/config_package/sale_url_cfg.ini'
            config = self.open_config_file(cfg_path)
            item = dict(item)
            self.process_data(item)
            if not item['name']:
                return "无效url"
            url_md5 = self.transformd5(item['url'])
            sql = """insert into url_info_all_t (name, province, city, district, bizcircle, url, datatype, taskstatus, url_md5)
                         values ('%s', '%s', '%s', '%s', '%s', '%s', '%s', %s, '%s');
                         """ % (item['name'], item['provice'], item['city'], item['district'], item['bizcircle'], item['url'],
                         item['datatype'], item['Taskstatus'], url_md5)
            logs.debug("sql: %s", sql)
            result_file = config.get(spider.spider_name, 'json_file')
            self.open_result_file(result_file, item)
            self.insert_sql_execute(sql)
            return item
        elif spider.name == "ershoufang_detail":
            cfg_path = './xiaoqu_url/config_package/sale_detail_cfg.ini'
            config = self.open_config_file(cfg_path)
            ip = get_ip_address('eth0')
            item = dict(item)
            self.process_data(item)
            result_file = '%s.%s.%s' % (ip, config.get(spider.spider_name, 'json_file'),
                    datetime.datetime.now().strftime('%Y%m%d'))
            self.open_result_file(result_file, item)
            sql = """
                      update url_info_all_t set taskstatus=1 where url_md5='%s'
                  """ % spider.tag
            logs.debug("sql: %s" % sql)
            self.update_sql_execute(sql)
            return item
