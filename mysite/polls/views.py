from django.shortcuts import render
from polls.models import Goods
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, reverse, redirect
import threading
import time
from .resources.Amazon import *
from .resources.Jingdong import *
from .resources.Suning import *
urls = {'Amazon': 'https://www.amazon.cn/s/ref=sr_pg_2?rh=i%3Aaps%2Ck%3A&keywords=',
        'Jingdong': 'https://search.jd.com/Search?&enc=utf-8&qrst=1&rt=1&stop=1&vt=2',
        'Suning': 'https://www.suning.com/'
        }
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
def init(kw):
    keyword = kw
    try:
        initialMount = 30
        # 这里需要为每一个网站分配爬取的数量，现在只有亚马逊一个
        # 开启一个新的线程，亚马逊，京东，天猫，苏宁分别是独立的线程。
        FirstThread = getInfoThread(keyword, "first", initialMount)
        FirstThread.start()
        FirstThread.join()
        # print(111)
        # 其他线程：……
    except Exception as e:
        print(str(e))
class getInfoThread(threading.Thread):
    threadId = 0
    website = {}
    def __init__(self, keyword, type, amount):
        self.id = getInfoThread.threadId
        getInfoThread.threadId += 1
        self.type = type
        self.keyword = keyword
        self.amount = amount
        threading.Thread.__init__(self)

    def run(self):
        if self.type == "first":
            self.multicrawler()
        elif self.type == "jingdong":
            option = webdriver.ChromeOptions()
            option.add_argument("headless")
            driver = webdriver.Chrome(chrome_options=option)
            JingdonggetInfo(driver,urls['Jingdong'],self.keyword,self.amount)
            driver.close()
        elif self.type == "amazon":
            option = webdriver.ChromeOptions()
            option.add_argument("headless")
            driver = webdriver.Chrome(chrome_options=option)
            AmazongetInfo(driver, urls['Amazon'], self.keyword, self.amount)
            driver.close()
        elif self.type == "suning":
            option = webdriver.ChromeOptions()
            option.add_argument("headless")
            driver = webdriver.Chrome(chrome_options=option)
            Suninggetinfo(driver, urls['Suning'], self.keyword, self.amount)
            driver.close()
    def multicrawler(self):
        option = webdriver.ChromeOptions()
        option.add_argument("headless")
        driver = webdriver.Chrome(chrome_options=option)
        amount = 30
        JingdonggetInfo(driver, urls['Jingdong'], self.keyword, amount//3)
        AmazongetInfo(driver, urls['Amazon'], self.keyword, amount//3)
        Suninggetinfo(driver,urls['Suning'],self.keyword,amount//3)
        driver.quit()

# 把参数传给html
def index(request):
    return render(request, "polls/index.html")
@csrf_exempt
def barrage(request):
    kw=request.POST.get("barrage_kw",None)
    good_list = Goods.objects.filter(keyword=kw)
    id_list=[i for i in range(len(good_list))]
    good_id=zip(good_list,id_list)
    context = {
        'goods': good_list,
        'id_incre':len(good_list),
        'good_id':good_id
    }
    return render(request, 'polls/barrage.html', context)
@csrf_exempt
def goods(request,kw):
    good_list=Goods.objects.filter(keyword=kw)
    paginator=Paginator(good_list,12)
    page=request.GET.get('page')
    try:
        context = {
            'goods': paginator.page(page)
        }
    except PageNotAnInteger:
        context = {
            'goods': paginator.page(1)
        }
    except EmptyPage:
        context = {
            'goods': paginator.page(paginator.num_pages)
        }
    return render(request,'polls/goods.html',context)
@csrf_exempt
def postKeyword(request):
    kw = request.POST.get('keyword', None)
    startsypder =True
    if len(Goods.objects.filter(keyword=kw))!=0:
        startsypder = False
        time.sleep(5)
    if startsypder:
        init(kw)
        amount = 30
        Amazon = getInfoThread(kw, "amazon", amount)
        Amazon.start()
        Jingdong = getInfoThread(kw, "jingdong", amount)
        Jingdong.start()
        Suning = getInfoThread(kw, "suning", amount)
        Suning.start()
        return redirect('polls:goods', kw=kw)
    else:
        return redirect('polls:goods', kw=kw)
