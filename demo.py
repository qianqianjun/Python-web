from selenium import webdriver
from lxml import etree
import time
driver = webdriver.Chrome()
driver.maximize_window()
def get_info(url, page):
    page = page + 1
    driver.get(url)
    driver.implicitly_wait(10)
    selector = etree.HTML(driver.page_source)
    with open('hello.html', 'w', encoding='utf-8') as f:
        f.write(driver.page_source)
    infos = selector.xpath('//div[@class="item J_MouserOnverReq  "]')
    for info in infos:
        goods = info.xpath('div/div/div/a/img/@alt')[0]
        price = info.xpath('div/div/div/strong/text()')[0]
        sell = info.xpath('div/div/div[@class="deal-cnt"]/text()')
        if sell:
            sells = sell[0]
        else:
            sells = 0
        shop = info.xpath('div[2]/div[3]/div[1]/a/span[2]/text()')[0]
        address = info.xpath('div[2]/div[3]/div[2]/text()')[0]
        commodity = {
            'goods': goods,
            'price': price,
            'sell': sells,
            'shop': shop,
            'address': address
        }
        # taobao.insert_one(commodity)
        print(commodity)
    if page <= 50:
        NextPage(url, page)
    else:
        pass


def NextPage(url, page):
    driver.get(url)
    driver.implicitly_wait(10)
    driver.find_element_by_xpath('//a[@trace="srp_bottom_pagedown"]').click()
    time.sleep(4)
    get_info(driver.current_url, page)


if __name__ == "__main__":
    url = 'https://www.taobao.com'
    driver.get(url)
    driver.implicitly_wait(10)
    driver.find_element_by_id('q').clear()
    driver.find_element_by_id('q').send_keys('男士短袖')
    driver.find_element_by_class_name('btn-search').click()
    get_info(driver.current_url, 1)