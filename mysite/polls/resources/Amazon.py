from lxml import etree
from ..models import *
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


def AmazongetInfo(driver, url, keyword, amount):

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
            # print(image)
            name = i.xpath('div/div[3]/div/a/h2/text()')
            # 这里判断两种页面的两种情况，根据不同的情况确定爬取的方式
            if len(name) != 0:
                try:

                    good.name = name[0]
                    link = i.xpath('div/div[@class="a-row a-spacing-mini"]/div/a/@href')[0]
                    # print(link)
                    good.url = link
                    price = i.xpath('div/div[5]/div[1]/a/span[2]/text()')[0]
                    # print(price)
                    good.price = price
                    # print(good.name, good.source)
                except:
                    pass
            else:
                try:
                    # 爬取含有广告标识的项目
                    name = i.xpath('div/div[4]/div[1]/a/h2/text()')
                    # print(name[0])
                    good.name = name
                    link1 = i.xpath('div/div[4]/div[1]/a/@href')
                    link = "https://www.amazon.cn" + link1[0]
                    # print(link)
                    good.url = link
                    price = i.xpath('div/div[last()]/div/a/span[2]/text()')[0]
                    # print(price)
                    good.price = price
                except:
                    pass
            good.source = "Amazon"
            if good.price != "" and good.name != "" and good.url != "" and good.image != "":
                resultSet.append(good)
                length += 1
                if length>=amount:
                    break
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
                             keyword=keyword)

    # driver.close()

