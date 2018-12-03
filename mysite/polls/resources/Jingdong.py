# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.common.exceptions import TimeoutException
# import threading
#
# import csv
# import time
# import random
from lxml import etree
from bs4 import BeautifulSoup
from ..models import *
class GoodItem(object):
    def __init__(self):
        #商品名称
        self.name=""
        #价格
        self.price=""
        #图片
        self.image=""
        #来源：亚马逊
        self.source=""
        #详情链接：
        self.url=""

# page=1

def JingdonggetInfo(driver,url,keyword,amount):
    # driver = webdriver.Chrome()
    length = 0
    resultSet = []
    page = 1
    driver.get(url + "&page=" + str(page) + "&keyword=" + keyword)
    while length < amount:
        source_code = driver.page_source
        selector = etree.HTML(source_code)
        with open('jd.html', 'w', encoding='utf-8') as f:
            f.write(driver.page_source)
        htmlfile = open('jd.html', 'r', encoding='utf-8')
        htmlhandle = htmlfile.read()
        soup = BeautifulSoup(htmlhandle, 'lxml')
        # infos=soup.find_all('li',attrs={'class':'gl-item'})
        # # for i in infos:
        address = []
        img1 = []
        price = []
        shop = []
        goods = []
        a = soup.find_all('div', attrs={'class': 'p-img'})
        for aa in a:
            if aa.parent.name == "div":
                if "gl-i-wrap" in aa.parent['class']:
                    address.append(aa.a['href'])
                    #print(aa.img['class'])
                    if aa.img['class']==['']:
                        img1.append(aa.img['src'])
                    elif aa.img['class']==['err-product']:
                        img1.append(aa.img['data-lazy-img'])
        p = soup.find_all('div', attrs={'class': 'p-price'})
        for pp in p:
            if pp.parent.name == "div":
                price.append(pp.i.string)
        s = soup.find_all('div', attrs={'class': 'p-shop'})
        for ss in s:
            if ss.parent.name == "div":
                shop.append(ss.a['title'])
        g = soup.find_all('div', attrs={'class': 'p-name'})
        for gg in g:
            if gg.parent.name == "div":
                goods.append(gg.a['title'])
        for i in range(len(address)):
            good = GoodItem()
            good.price = price[i]
            good.name = goods[i]
            good.source = 'jingdong'
            good.url = address[i]
            good.image=img1[i]
            resultSet.append(good)
            # print(good.name,good.price,good.url,good.image)
            length+=1
            if length>=amount:
                break
            # if good.price != "" and good.name != "" and good.image != "":
            #     resultSet.append(good)
            #     length += 1
            #     flag = True
            # if not flag:
            #     break
            if length < amount:
                # driver.find_element_by_xpath('//div[@id="search-main-wrapper"]//div[@id="centerBelowMinus"]//a[@id="pagnNextLink"]').click()
                # next=selector.xpath('//div[@id="search-main-wrapper"]//div[@id="centerBelowMinus"]//a[@id="pagnNextLink"]/@href')
                page += 1
                driver.get(url + "&page=" + str(page) + "&keyword=" + keyword)
    # driver.close()

    for item in resultSet:
            Goods.objects.create(name=item.name, source=item.source, url=item.url, picture=item.image, price=item.price,keyword=keyword)