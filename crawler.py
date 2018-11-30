from selenium import webdriver
from lxml import etree
import requests
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
def get_info(url,keyword,amount):
    resultSet=[]
    num = 0
    control_times = 10

    option = webdriver.ChromeOptions()
    option.add_argument("--start-maximized")
    option.add_argument("--disable-infobars")
    # option.add_argument("headless")
    browser = webdriver.Chrome(chrome_options=option)#executable_path='chromedriver.exe'
    try:
        browser.get(url)
        # browser.implicitly_wait(5)
        input_str = browser.find_element_by_id('searchKeywords')
        input_str.send_keys(keyword)
        button = browser.find_element_by_id('searchSubmit')
        button.click()
        time.sleep(5)
    except :
        print("Error! Please check your Internet connection.")

    pageNumber = 2
    while num<amount:
        for i in range(4):
            js = "window.scrollTo(0,{times}*window.innerHeight);".format(times=(i+1)*5)
            browser.execute_script(js)
            time.sleep(3)
        judge = 0
        selector = etree.HTML(browser.page_source)
        infos = selector.xpath('/html/body/div/div/ul[@class="general clearfix"]/li')
        for i in infos:
            k = i.xpath('div/div/div[@class="res-info"]/div[@class="price-box"]/span[@class="def-price"]/text()')
            # print(k)
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
            good.image=infos[i].xpath('div/div/div/div[@class="img-block"]/a/img/@src') #photo
            good.url = infos[i].xpath('div/div/div/div[@class="title-selling-point"]/a/@href')#detail page url
            good.name = name #name of good
            good.price = price
            num += 1
            resultSet.append(good)
            #img
            # print(infos[i].xpath('div/div/div/div[@class="img-block"]/a/img/@src'))
            #price
            # print(infos[i].xpath('div/div/div[@class="res-info"]/div[@class="price-box"]/span[@class="def-price"]/text()'))
            # print(price)
            #name
            # print(infos[i].xpath('div/div/div/div[@class="title-selling-point"]/a/text()'))
            # print(name)
            #detail page
            # print(infos[i].xpath('div/div/div/div[@class="title-selling-point"]/a/@href'))
            # print('\n')
        # print(len(resultSet))
        # print(judge)
        # print(len(infos))

        try:
            next_page = browser.find_element_by_id("bottomPage")
            next_page.send_keys(pageNumber)
            next_button = browser.find_element_by_name("ssdsn_search_bottom_page")
            next_button.click()
            pageNumber += 1
        except:
            print("Not enough information provided by the Website")
            break

        control_times -= 1
        if control_times<0:
            print("Sorry, the internet situation is too bad to get enough information.")
            break
    time.sleep(10)
    browser.quit()
    return resultSet

if __name__ == '__main__':
    goodName = input("Please input good's name\n")
    get_info(url,goodName,100)