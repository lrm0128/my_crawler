#!/usr/bin/env python
# coding=utf-8

import MySQLdb


class MySQLConn(object):
    db = MySQLdb.connect(
        host='120.24.90.29',
        user='cnfsdata1',
        passwd='cnfsdata1',
        db='cnfsdata',
        charset='utf8',
    )
    cursor = db.cursor()

    def inser_data(self, sql):
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except Exception as e:
            return "Some thing is wrong~"

sql = '''
insert into url_xiaoqu_all_t (id, name, province, city, district, bizcircle, url, url_md5, site, taskstatus)
 values ('876b7145fc7805b85f8eeb12f518b68f', '迎宾小区', '吉林','长春', '绿','http://yingbinxiaoqu0431.fang.com/', 'fangtianxia', '0');

'''
