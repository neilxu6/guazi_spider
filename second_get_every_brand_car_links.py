#-*-coding:utf-8-*-
import time
import random
import pymongo
import requests
from bs4 import BeautifulSoup


# 取出某品牌车的所有在售链接--spider2
def get_every_brand_car_links(start_url):
    client = pymongo.MongoClient('localhost', 27017)
    guazi_web = client['guazi_web']
    cars_info = guazi_web['cars_info']
    # 主域名
    host_url='http://m.guazi.com'
    # 头标签——使用手机来爬取
    headers={
        'Connection':'keep-alive',
        'User-Agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1',
    }
    # http://cn-proxy.com/
    proxy_list = [
        'http://101.230.8.69:8000',
        'http://120.90.6.92:8080',
        'http://120.204.85.29:3128'
    ]
    proxy_ip = random.choice(proxy_list)  # 随机获取代理ip
    proxies = {'http': proxy_ip}
    # ,proxies=proxies
    # 发起请求
    web_data=requests.get(start_url,headers=headers)
    time.sleep(4)
    # 构造BeautifulSoup
    soup=BeautifulSoup(web_data.text,'lxml')
    # 取出链接
    links=soup.select('body > div.line-list.js-list-page > section.mod-list.js-car-list > ul > li > a')
    titles=soup.select('body > div.line-list.js-list-page > section.mod-list.js-car-list > ul > li > a > h3.car-name')
    dates=soup.select('body > div.line-list.js-list-page > section.mod-list.js-car-list > ul > li > a > div.car-km > span')
    journey=soup.select('body > div.line-list.js-list-page > section.mod-list.js-car-list > ul > li > a > div.car-km > span')
    prices=soup.select('body > div.line-list.js-list-page > section.mod-list.js-car-list > ul > li > a > div.car-price > strong')
    # 编码问题——用的是什么码？可不可以转换成utf-8？？？？？
    # 已解决：.encode('ISO-8859-1').decode('utf-8')
    for link,title,price,date,journey in zip(links,titles,prices,dates,journey):
            link = host_url+link.get('href').encode('ISO-8859-1').decode('utf-8')
            title =title.text.encode('ISO-8859-1').decode('utf-8')
            price=price.text.encode('ISO-8859-1').decode('utf-8')
            date=date.text.split('/')[0].encode('ISO-8859-1').decode('utf-8')
            journey=journey.text.split('/')[1].encode('ISO-8859-1').decode('utf-8')
            cars_info.insert({'title':title,'price':price,'date': date,'journey':journey,'link':link})


def get_more_cars_detail():
    # 连接数据库
    client = pymongo.MongoClient('localhost', 27017)
    guazi_web = client['guazi_web']
    brand_links = guazi_web['brand_links']
    print('==================> 开 始 获 得 二 手 车 信 息 <===================\n')
    for each_page_number in range(7,51,1):
        print('||=====>开始 抓取所有品牌二手车第 {} 页的信息<=====||\n'.format(each_page_number))
        # 从brand_links表中依次取品牌链接
        for i in brand_links.find():
            start_url = 'http://m.guazi.com/sh/buy/o{}/?url='.format(each_page_number)
            print('==============================================================')
            print('>==开始抓取 {} 车型的'.format(str(i['brand_link']).split('/')[-2])+'第 {} 页的二手车信息==<\n'.format(each_page_number))
            # print(str(start_url)+str(i['brand_link']).split('/')[-2])
            get_every_brand_car_links(str(start_url)+str(i['brand_link']).split('/')[-2])
            print('>==结束抓取 {} 车型的'.format(str(i['brand_link']).split('/')[-2])+'第 {} 页的二手车信息==<'.format(each_page_number))
        print('||=====>结束 抓取所有品牌二手车第 {} 页的信息<=====||'.format(each_page_number))
        print('======================================================================')
    print('==================> 已 获 得 所 有 车 型 的 信 息 <===================\n')



