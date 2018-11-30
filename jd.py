from selenium import webdriver
from lxml import etree
from bs4 import BeautifulSoup
browser = webdriver.Chrome()
browser.get('https://www.jd.com/')
browser.implicitly_wait(10)
browser.find_element_by_css_selector("[class='QQ-icon']").click()
browser.implicitly_wait(10)
browser.switch_to.frame('ptlogin_iframe')
browser.implicitly_wait(10)
print(browser.page_source)
browser.find_element_by_id("switcher_plogin").click()
#browser.find_element_by_class_name("img_out_focus").click()
browser.find_element_by_class_name("inputstyle").send_keys('1905946527')
browser.find_element_by_css_selector("[class='inputstyle password']").send_keys('')
browser.find_element_by_id("login_button").click()
browser.find_element_by_id("key").send_keys('iphone8')
browser.find_element_by_class_name("button").click()
source_code=browser.page_source
print(source_code)
selector=etree.HTML(source_code)
with open('hello.html','w',encoding='utf-8') as f:
    f.write(browser.page_source)
htmlfile=open('hello.html','r',encoding='utf-8')
htmlhandle=htmlfile.read()
soup=BeautifulSoup(htmlhandle,'lxml')
infos=soup.find_all('li',attrs={'class':'gl-item'})
count=0
# for i in infos:
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
    commodity = {
        'goods': goods[i],
        'price': price[i],
        'shop': shop[i],
        'address': address[i]
    }
    print(commodity)
