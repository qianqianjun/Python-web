from selenium import webdriver
from ..models import *
from lxml import etree
import time
url = 'https://www.suning.com/'
class GoodItem(object):
    def __init__(self):
        #商品名称
        self.name=""
        #价格
        self.price=""
        #图片
        self.image=""
        #来源：苏宁
        self.source=""
        #详情链接：
        self.url=""
def Suninggetinfo(driver,url,keyword,amount):
    resultSet=[]
    num = 0
    # control_times = 10
    browser = driver
    # option = webdriver.ChromeOptions()
    # option.add_argument("--start-maximized")
    # option.add_argument("--disable-infobars")
    # option.add_argument("headless")
    # browser = webdriver.Chrome(chrome_options=option)#executable_path='chromedriver.exe'
    try:
        browser.get(url)
        input_str = browser.find_element_by_id('searchKeywords')
        input_str.send_keys(keyword)
        button = browser.find_element_by_id('searchSubmit')
        button.click()
        # time.sleep(1)
    except :
        print("Error! Please check your Internet connection.")
    judge = 0
    selector = etree.HTML(browser.page_source)
    infos = selector.xpath('/html/body/div/div/ul[@class="general clearfix"]/li')
    for i in infos:
        k = i.xpath('div/div/div[@class="res-info"]/div[@class="price-box"]/span[@class="def-price"]/text()')
        if (len(k)== 1 and k[0]=='\n') or len(k)==0:
            judge += 1
    infoNumber = len(infos)
    for i in range(infoNumber-judge):
        price = 0
        for j in infos[i].xpath('div/div/div[@class="res-info"]/div[@class="price-box"]/span[@class="def-price"]/text()'):
            if j != '\n':
                price = int(j)
        name = ""
        for j in infos[i].xpath('div/div/div/div[@class="title-selling-point"]/a/text()'):#deal name of good
            if j != '\n':
                name += j
        good = GoodItem()
        good.source="苏宁"
        good.image=infos[i].xpath('div/div/div/div[@class="img-block"]/a/img/@src')[0] #photo
        good.url = infos[i].xpath('div/div/div/div[@class="title-selling-point"]/a/@href')[0]#detail page url
        good.name = name #name of good
        good.price = price
        num += 1
        if num>amount:
            break
        resultSet.append(good)
    # control_times -= 1
    # if control_times<0:
    #     print("Sorry, the internet situation is too bad to get enough information.")

    # print(len(resultSet))
    # for i in resultSet:
    #     print(i.price,i.name,i.url,i.image)
    #     print()
    # browser.quit()
    for item in resultSet:
        #增加数据验证的支持：防止url等太长添加不进去
        if item.price != "" and item.name != "" and item.url != "" and item.image != "" and len(
                item.url) <= 1000 and len(item.image) <= 300 and len(item.price) < 20 \
                and len(item.name) < 200:
            continue
        Goods.objects.create(name=item.name, source=item.source, url=item.url, picture=item.image, price=item.price,keyword=keyword)
