# -*- coding: utf-8 -*-
import time
import json
import requests
import mysql.connector
from lxml import etree
from selenium import webdriver


def enter_page_and_get_json(j):
    global fund_code, fund_name, fund_type, xpl
    url_name = driver.find_element_by_xpath('//*[@id="ctl00_cphMain_gridResult"]/tbody/tr['+j+']/td[3]/a')
    url = url_name.get_attribute("href")
    response = requests.request('get', url)
    fund_xpath = etree.HTML(response.text)
    fund_code = fund_xpath.xpath('//*[@id="qt_fund"]/span[1]/text()')[0][:6]
    fund_name = fund_xpath.xpath('//*[@id="qt_fund"]/span[1]/text()')[0][7:]
    fund_type = fund_xpath.xpath('//*[@id="qt_base"]/ul[3]/li[1]/span/text()')[0]
    url1 = 'http://cn.morningstar.com/handler/quicktake.ashx?command=rating&fcid=' + url[-10:]
    wbdata = requests.get(url1).text  # 对HTTP响应的数据JSON化.
    data = json.loads(wbdata)
    # print(data)
    xpl = data['RiskAssessment'][-1]['Year3']
    return fund_code, fund_name, fund_type, xpl


def deposit(fund_code1, fund_name1, fund_type1, xpl1):
    cur.execute("INSERT INTO xiapulv_data"
                "(num, fund_code, fund_name, fund_type, xpl)"
                "VALUES(null, %s, %s, %s, %s)",
                (fund_code1, fund_name1, str(fund_type1), xpl1))


if __name__ == '__main__':
    conn = mysql.connector.connect(user='root', password='a4592948',
                                   host='localhost', port='3306',
                                   database='fund', use_unicode=True)
    cur = conn.cursor()
    driver = webdriver.Chrome(r'C:\Users\Zhouxiong\AppData\Local\Google\Chrome\Application\chromedriver.exe')  # 打开谷歌浏览器
    driver.get("http://cn.morningstar.com/quickrank/default.aspx")
    # print(driver.page_source)
    page_num = 1
    while page_num <= 8:
        for i in range(2, 27):
            i = str(i)
            try:
                enter_page_and_get_json(i)
                try:
                    deposit(fund_code, fund_name, fund_type, xpl)
                except KeyError:
                    print(''+fund_code+'无夏普率比')
                    continue
            except KeyError:
                continue
        driver.find_element_by_link_text(">").click()
        page_num += 1
        time.sleep(3)
    conn.commit()
    cur.close()
    conn.close()
    driver.quit()
