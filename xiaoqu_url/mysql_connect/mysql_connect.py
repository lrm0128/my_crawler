#!/usr/bin/env python
# coding=utf-8

import MySQLdb
from xiaoqu_url.log_package.log_file import logs


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
            logs.debug("Some thing is wrong~: %s" % e)

    def select_data(self, sql):
        data = ''
        try:
            self.cursor.execute(sql)
            data = self.cursor.fetchall()
        except Exception as e:
            logs.debug("select failed : %s" % e)
        return data

    def update_to_table(self, sql):
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except Exception as e:
            logs.debug('update failed : %s' % e)

"""
sql = '''update url_xiaoqu_all_t set taskstatus="0" where city="长春";'''
sql2 = '''select count(taskstatus) from url_xiaoqu_all_t where city="长春" and taskstatus="0";'''
sql_conn = MySQLConn()
print sql_conn.select_data(sql2)
"""