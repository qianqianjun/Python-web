# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.common.exceptions import TimeoutException
# import threading
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
# def JingdonggetInfo(driver,url,keyword,amount):
#     length = 0
#     resultSet = []
#     page = 1
#     driver.get(url + "&page=" + str(page) + "&keyword=" + keyword)
#     while length < amount:
#         source_code = driver.page_source
#         selector = etree.HTML(source_code)
#         with open('jd.html', 'w', encoding='utf-8') as f:
#             f.write(driver.page_source)
#         htmlfile = open('jd.html', 'r', encoding='utf-8')
#         htmlhandle = htmlfile.read()
#         soup = BeautifulSoup(htmlhandle, 'lxml')
#         address = []
#         img1 = []
#         price = []
#         shop = []
#         goods = []
#         a = soup.find_all('div', attrs={'class': 'p-img'})
#         for aa in a:
#             if aa.parent.name == "div":
#                 if "gl-i-wrap" in aa.parent['class']:
#                     address.append(aa.a['href'])
#                     if aa.img['class']==['']:
#                         img1.append(aa.img['src'])
#                     elif aa.img['class']==['err-product']:
#                         img1.append(aa.img['data-lazy-img'])
#         p = soup.find_all('div', attrs={'class': 'p-price'})
#         for pp in p:
#             if pp.parent.name == "div":
#                 price.append(pp.i.string)
#         s = soup.find_all('div', attrs={'class': 'p-shop'})
#         for ss in s:
#             if ss.parent.name == "div":
#                 shop.append(ss.a['title'])
#         g = soup.find_all('div', attrs={'class': 'p-name'})
#         for gg in g:
#             if gg.parent.name == "div":
#                 goods.append(gg.a['title'])
#         for i in range(len(address)):
#             good = GoodItem()
#             good.price = price[i]
#             good.name = goods[i]
#             good.source = 'jingdong'
#             good.url = address[i]
#             good.image=img1[i]
#             resultSet.append(good)
#             length+=1
#             if length>=amount:
#                 break
#             if good.price != "" and good.name != "" and good.image != "":
#                 resultSet.append(good)
#                 length += 1
#                 flag = True
#             if not flag:
#                 break
#             if length < amount:
#                 page += 1
#                 driver.get(url + "&page=" + str(page) + "&keyword=" + keyword)
#     for item in resultSet:
#             Goods.objects.create(name=item.name, source=item.source, url=item.url, picture=item.image, price=item.price,keyword=keyword)
def JingdonggetInfo(driver, url, keyword, amount):
    length = 0
    resultSet = []
    page = 1
    driver.get(url + "&page=" + str(page) + "&keyword=" + keyword)
    with open('jd.html', 'w', encoding='utf-8') as f:
        f.write(driver.page_source)
    htmlfile = open('jd.html', 'r', encoding='utf-8')
    htmlhandle = htmlfile.read()
    while length < amount:
        selector = etree.HTML(htmlhandle)
        infos = selector.xpath('//ul[@class="gl-warp clearfix"]/li')
        for i in infos:
            good = GoodItem()
            try:
                image = i.xpath("div/div[@class='p-img']/a/img/@src")
                if len(image) == 0:
                    image = i.xpath("div/div[@class='p-img']/a/img/@data-lazy-img")[0]
                else:
                    image = i.xpath("div/div[@class='p-img']/a/img/@src")[0]
                good.image = image
                # print(image)
                price = i.xpath('div/div[@class="p-price"]/strong/i/text()')[0]
                good.price = price
                # print(price)
                name = i.xpath("div/div[@class='p-name p-name-type-2']/a/em/text()")[0]
                good.name = name
                # print(name)
                url = i.xpath("div/div[@class='p-img']/a/@href")[0]
                good.url = url
                # print(url)
                # print([good.name,good.image,good.url,good.price])
            except:
                pass
            good.source = "JingDong"
            if good.price != "" and good.name != "" and good.url != "" and good.image != "" and len(
                    good.url) <= 1000 and len(good.image) <=300 and len(good.price)<20 \
                    and len(good.name)<200:
                resultSet.append(good)
                length += 1
                if length >= amount:
                    break
        if length < amount:
            page += 1
            driver.get(url + "&page=" + str(page) + "&keyword=" + keyword)
    for item in resultSet:
        Goods.objects.create(name=item.name, source=item.source, url=item.url, picture=item.image, price=item.price,
                             keyword=keyword)