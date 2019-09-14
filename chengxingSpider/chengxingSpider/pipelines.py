# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import mysql.connector


class chengxingspiderPipeline(object):
    def __init__(self):
        self.conn = mysql.connector.connect(user='root', password='a4592948',
                                            host='localhost', port='3306',
                                            database='fund', use_unicode=True)
        self.cur = self.conn.cursor()
        # 重写close_spider回调方法，用于关闭数据库资源

    def close_spider(self, spider):
        print('-关闭数据库资源-')
        # 关闭游标
        self.cur.close()
        # 关闭连接
        self.conn.close()

    def process_item(self, item, spider):
        self.cur.execute("INSERT INTO fund_data"
                         "(num, fund_code, fund_name, fund_price, date)"
                         "VALUES(null, %s, %s, %s, %s)",
                         (str(item['fund_code']), str(item['fund_name']), str(item['fund_price']), str(item['date'])))
        self.conn.commit()



    # def process_item(self, item, spider):
    #     print('基金名称：', item['fund_name'])
    #     print('基金净值：', item['fund_price'])
    #     print('日期：', item['date'])

