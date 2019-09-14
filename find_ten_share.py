# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re
import json
import requests
from lxml import etree
import mysql.connector

conn = mysql.connector.connect(user='root', password='a4592948',
                               host='localhost', port='3306',
                               database='fund', use_unicode=True)
cur = conn.cursor()

driver = webdriver.Chrome(r'C:\Users\Zhouxiong\AppData\Local\Google\Chrome\Application\chromedriver.exe')  # 打开谷歌浏览器
driver.get("http://cn.morningstar.com/fundselect/default.aspx")
driver.find_element_by_id("ctl00_cphMain_cblGroup_0").click()
driver.find_element_by_id("ctl00_cphMain_cblCategory_0").click()
driver.find_element_by_id("ctl00_cphMain_cblStarRating_0").click()
driver.find_element_by_id("ctl00_cphMain_btnGo").click()
print(driver.page_source)

page_num = 1
while page_num <= 2:
    for i in range(2, 27):
        i = str(i)
        try:
            url_name = driver.find_element_by_xpath('//*[@id="ctl00_cphMain_gridResult"]/tbody/tr['+i+']/td[3]/a')
            url = url_name.get_attribute("href")
            url1 = 'http://cn.morningstar.com/handler/quicktake.ashx?command=portfolio&fcid=' + url[-10:]
            wbdata = requests.get(url1).text
            # 对HTTP响应的数据JSON化.
            data = json.loads(wbdata)
            # print(data)
            datas = data['Top10StockHoldings']
            #对索引出来的JSON数据进行遍历和提取
            for n in range(10):
                try:
                    share_name = datas[n]['HoldingName']
                    cur.execute("INSERT INTO share_data"
                                "(id, share_name)"
                                "VALUES(null, %s)",
                                (str(share_name),))
                except:
                    print(url)
                    continue
        except:
            continue

    driver.find_element_by_link_text(">").click()
    page_num += 1
    time.sleep(5)
conn.commit()
cur.close()
conn.close()
driver.quit()

