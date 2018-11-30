from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import threading

import csv
import time
import random
from lxml import etree
from bs4 import BeautifulSoup
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
class getInfoThread(threading.Thread):
    threadId=0
    website={}
    #这里规定爬取的起始url:
    website['jingdong'] = "https://search.jd.com/Search?&enc=utf-8&qrst=1&rt=1&stop=1&vt=2"
    def __init__(self,keyword,type,amount):
        self.id=getInfoThread.threadId
        getInfoThread.threadId+=1
        self.type=type
        self.keyword=keyword
        self.amount=amount
        threading.Thread.__init__(self)
    def run(self):
        if self.type=="amazon":
            url=getInfoThread.website[self.type]
            AmazongetInfo(url,self.keyword,self.amount)
        else:
            if self.type=='jingdong':
                url = getInfoThread.website[self.type]
                print(url)
                JingDonggetInfo(url, self.keyword, self.amount)
def JingDongInfo(url,keyword,amount):
    driver = webdriver.Chrome()
    length = 0
    resultSet = []
    page = 1
    driver.get(url + "&page=" + str(page)+"&keyword=" + keyword)
    while length<amount:
        source_code=driver.page_source
        selector=etree.HTML(source_code)
        with open('jd.html','w',encoding='utf-8') as f:
            f.write(driver.page_source)
        htmlfile=open('jd.html','r',encoding='utf-8')
        htmlhandle=htmlfile.read()
        soup=BeautifulSoup(htmlhandle,'lxml')
        # infos=soup.find_all('li',attrs={'class':'gl-item'})
        # # for i in infos:
        address=[]
        img1=[]
        price=[]
        shop=[]
        goods=[]
        a=soup.find_all('div', attrs={'class': 'p-img'})
        for aa in a:
            if aa.parent.name=="div":
                if "gl-i-wrap" in aa.parent['class']:
                    # print(aa)
                    # print(aa.img['class'])
                    address.append(aa.a['href'])
                    # img1.append(aa.img['src'])
        p=soup.find_all('div', attrs={'class': 'p-price'})
        for pp in p:
            if pp.parent.name=="div":
                price.append(pp.i.string)
        s=soup.find_all('div', attrs={'class': 'p-shop'})
        for ss in s:
            if ss.parent.name == "div":
                shop.append(ss.a['title'])
        g = soup.find_all('div', attrs={'class': 'p-name'})
        for gg in g:
            if gg.parent.name == "div":
                goods.append(gg.a['title'])
        for i in range(len(address)):
            good = GoodItem()

            good.price=price[i]
            good.name=goods[i]
            good.source='jingdong'
            good.url=address[i]
            if good.price != "" and good.name != "" and good.link != "" and good.image != "":
                resultSet.append(good)
                length += 1
                flag = True
            if not flag:
                break
            if length < amount:
                # driver.find_element_by_xpath('//div[@id="search-main-wrapper"]//div[@id="centerBelowMinus"]//a[@id="pagnNextLink"]').click()
                # next=selector.xpath('//div[@id="search-main-wrapper"]//div[@id="centerBelowMinus"]//a[@id="pagnNextLink"]/@href')
                page += 1
                driver.get(url + "&page=" + str(page)+"&keyword=" + keyword)
    driver.close()
def init():
    keyword='iphone8'
    amount=int(40)
    #这里需要为每一个网站分配爬取的数量，现在只有亚马逊一个
    amountJingDong=amount//1
    #开启一个新的线程，亚马逊，京东，天猫，苏宁分别是独立的线程。
    jd=getInfoThread(keyword,"jingdong",amountJingDong)
    jd.start()