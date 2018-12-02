from django.shortcuts import render
from polls.models import Goods
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, reverse, redirect
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from selenium import webdriver
from lxml import etree
from tkinter import *
import threading
import time
#把参数传给html
def index(request):
    return render(request,"polls/index.html")
def barrage(request):
	return render(request,"polls/barrage.html")

@csrf_exempt
def goods(request,kw):

    good_list=Goods.objects.filter(keyword=kw)
    context = {
        'goods': good_list
    }
    return render(request,'polls/goods.html',context)

@csrf_exempt
def postKeyword(request):
    kw = request.POST.get('keyword', None)

    class GoodItem(object):
        def __init__(self):
            # 商品名称
            self.name = ""
            # 价格
            self.price = ""
            # 图片
            self.image = ""
            # 来源：亚马逊
            self.source = ""
            # 详情链接：
            self.url = ""

    class getInfoThread(threading.Thread):
        threadId = 0
        website = {}
        # 这里规定爬取的起始url:
        website["amazon"] = "https://www.amazon.cn/s/ref=sr_pg_2?rh=i%3Aaps%2Ck%3A&keywords="
        website["tianmao"] = ""

        def __init__(self, keyword, type, amount):
            self.id = getInfoThread.threadId
            getInfoThread.threadId += 1
            self.type = type
            self.keyword = keyword
            self.amount = amount
            threading.Thread.__init__(self)

        def run(self):
            if self.type == "amazon":
                url = getInfoThread.website[self.type]
                AmazongetInfo(url, self.keyword, self.amount)
            else:
                # 其他网站的爬取函数
                pass

    def AmazongetInfo(url, keyword, amount):
        option = webdriver.ChromeOptions()
        option.add_argument("headless")
        # driver = webdriver.Chrome(chrome_options=option)
        driver = webdriver.Chrome()
        url = url + keyword
        length = 0
        resultSet = []
        page = 1
        driver.get(url + "&page=" + str(page))
        # driver.implicitly_wait(10)
        # print(driver.page_source)
        while length < amount:
            selector = etree.HTML(driver.page_source)
            infos = selector.xpath('//ul[@id="s-results-list-atf"]/li')
            flag = False
            for i in infos:
                print("-----------------------------------------")
                good = GoodItem()
                try:
                    image = i.xpath('div/div[@class="a-row a-spacing-base"]/div/div/a/img/@src')[0]
                    good.image = image
                except:
                    break
                print(image)
                name = i.xpath('div/div[3]/div/a/h2/text()')
                # 这里判断两种页面的两种情况，根据不同的情况确定爬取的方式
                if len(name) != 0:
                    try:

                        good.name = name[0]
                        link = i.xpath('div/div[@class="a-row a-spacing-mini"]/div/a/@href')[0]
                        print(link)
                        good.url = link
                        price = i.xpath('div/div[5]/div[1]/a/span[2]/text()')[0]
                        print(price)
                        good.price = price
                        print(good.name, good.source)
                    except:
                        pass
                else:
                    try:
                        # 爬取含有广告标识的项目
                        name = i.xpath('div/div[4]/div[1]/a/h2/text()')
                        print(name[0])
                        good.name = name
                        link1 = i.xpath('div/div[4]/div[1]/a/@href')
                        link = "https://www.amazon.cn" + link1[0]
                        print(link)
                        good.url = link
                        price = i.xpath('div/div[last()]/div/a/span[2]/text()')[0]
                        print(price)
                        good.price = price
                    except:
                        pass
                good.source = "Amazon"
                if good.price != "" and good.name != "" and good.url != "" and good.image != "":
                    resultSet.append(good)
                    length += 1
                    flag = True
            if not flag:
                break
            if length < amount:
                # driver.find_element_by_xpath('//div[@id="search-main-wrapper"]//div[@id="centerBelowMinus"]//a[@id="pagnNextLink"]').click()
                # next=selector.xpath('//div[@id="search-main-wrapper"]//div[@id="centerBelowMinus"]//a[@id="pagnNextLink"]/@href')
                page += 1
                driver.get(url + "&page=" + str(page))
        for item in resultSet:
            Goods.objects.create(name=item.name, source=item.source, url=item.url, picture=item.image, price=item.price,
                                 keyword=kw)
        driver.close()

    def init():
        keyword = kw
        try:
            amount = 1
            # 这里需要为每一个网站分配爬取的数量，现在只有亚马逊一个
            amountAmazon = amount
            # 开启一个新的线程，亚马逊，京东，天猫，苏宁分别是独立的线程。
            amazon = getInfoThread(keyword, "amazon", amountAmazon)
            amazon.start()
            # 其他线程：……
        except Exception as e:
            print(str(e))
    init()
    time.sleep(20)
    return redirect('polls:goods', kw=kw)



