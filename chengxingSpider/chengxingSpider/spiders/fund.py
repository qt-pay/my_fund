# -*- coding: utf-8 -*-
import scrapy
from lxml import etree
import time

from chengxingSpider.items import ChengxingspiderItem



class FundSpider(scrapy.Spider):
    name = 'fund'
    allowed_domains = ['cn.morningstar.com/quicktake/']
    fund_list = ['0P0000Z821', 'F0000003VJ', '0P00016WFU', 'F000000416', 'F0000004AI', '0P00015HFT', 'F0000003ZX', '0P000147K8', '0P0000P5UD', '0P0001606X']

    start_urls = [f'http://cn.morningstar.com/quicktake/{page}' for page in fund_list]
        # time.sleep(3)

    def parse(self, response):
        # print(type(response))
        # print(dir(response))
        # print(response.status)

        # 把网页变成xpath结构
        fund_xpath = etree.HTML(response.text)
        item = ChengxingspiderItem()
        fund_name = fund_xpath.xpath('//*[@id="qt_fund"]/span[1]/text()')
        fund_price = fund_xpath.xpath('//*[@id="qt_base"]/ul[1]/li[2]/span/text()')
        date = fund_xpath.xpath('//*[@id="qt_base"]/ul[1]/li[3]/text()')
        # print(type(li))
        # print(li)
        item['fund_code'] = fund_name[0][:6]
        item['fund_name'] = fund_name[0][7:]
        item['fund_price'] = fund_price[0]
        item['date'] = date[0][5:]
        # print(fund_name[0])
        # print(date[0])
        print(len(date[0]))
        # print(type(item['date']))
        # print(type(fund_price))
        # print(dir(fund_price))
        # print(len(str(date)))
        # print(str(date)[-12:-1])
        return item
