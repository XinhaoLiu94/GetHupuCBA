# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from twisted.enterprise import adbapi
import MySQLdb
import MySQLdb.cursors

class HupuPipeline(object):
    def process_item(self, item, spider):
        return item

class MysqlTwistedPipeline(object):
    def __init__(self,dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls,settings):
        dbparm = dict(
            host = settings["MYSQL_HOST"],
            db = settings["MYSQL_DBNAME"],
            user = settings["MYSQL_USER"],
            password = settings["MYSQL_PASSWORD"],
            charset = "utf8",
            cursorclass = MySQLdb.cursors.DictCursor,
            use_unicode = True
        )

        dbpool = adbapi.ConnectionPool("MySQLdb",**dbparm)

        return cls(dbpool)

    def process_item(self,item,spider):
        query = self.dbpool.runInteraction(self.do_insert,item)
        query.addErrback(self.handle_error,item,spider)

    def handle_error(self, failure,item,spider):
        print(failure)

    def do_insert(self,cursor,item):
        insert_sql = """
                insert into hupuCBA (title , author , post_date ,max_praise_nums ,reply_nums)
                values (%s, %s, %s, %s, %s)
        """
        cursor.execute(insert_sql,(item["title"],item["author"],item["post_date"],item["max_praise_nums"],item["reply_nums"]))