from selenium import webdriver
def main():
    url = "https://search.jd.com/Search?&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&"
    keyword=input("请示输入keyword\n")
    # page = 7 & keyword = iphone8
    driver=webdriver.Chrome()
    url=url+"keyword="+keyword+"&"
    page=1
    while page<20:
        driver.get(url+"page="+str(page))
        with open(str(page)+".html",'w',encoding='utf-8') as f:
            f.write(driver.page_source)
        page+=2
    driver.close()
if __name__ == '__main__':
    main()
