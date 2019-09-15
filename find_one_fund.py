# -*- coding: utf-8 -*-
import time
import requests
import mysql.connector
from lxml import etree
from selenium import webdriver


def enter_page_and_get_data(fund_code1):
    global fund_name, fund_price, date, driver
    driver = webdriver.Chrome(r'C:\Users\Zhouxiong\AppData\Local\Google\Chrome\Application\chromedriver.exe')
    driver.get("http://cn.morningstar.com/quickrank/default.aspx")
    time.sleep(5)
    driver.find_element_by_id("ctl00_cphMain_txtFund").click()
    driver.find_element_by_id("ctl00_cphMain_txtFund").clear()
    driver.find_element_by_id("ctl00_cphMain_txtFund").send_keys(str(fund_code1))
    driver.find_element_by_id("ctl00_cphMain_btnGo").click()
    # print(driver.page_source)
    url_name = driver.find_element_by_xpath('//*[@id="ctl00_cphMain_gridResult"]/tbody/tr[2]/td[4]/a')
    url = url_name.get_attribute("href")
    # print(url)
    response = requests.request('get', url)
    fund_xpath = etree.HTML(response.text)
    fund_name = fund_xpath.xpath('//*[@id="qt_fund"]/span[1]/text()')[0][7:]
    fund_price = fund_xpath.xpath('//*[@id="qt_base"]/ul[1]/li[2]/span/text()')[0]
    date = fund_xpath.xpath('//*[@id="qt_base"]/ul[1]/li[3]/text()')[0][5:]
    return fund_name, fund_price, date


def deposit(fund_code1, fund_name1, fund_price1, date1):
    cur.execute("INSERT INTO fund_data"
                "(num, fund_code, fund_name, fund_price, date)"
                "VALUES(null, %s, %s, %s, %s)",
                (str(fund_code1), str(fund_name1), str(fund_price1), str(date1)))


if __name__ == '__main__':
    fund_code = input('请输入基金代码：')
    # print(fund_code)
    enter_page_and_get_data(fund_code)
    conn = mysql.connector.connect(user='root', password='a4592948',
                                   host='localhost', port='3306',
                                   database='fund', use_unicode=True)
    cur = conn.cursor()
    deposit(fund_code, fund_name, fund_price, date)
    conn.commit()
    cur.close()
    conn.close()
    driver.quit()
