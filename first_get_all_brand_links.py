#coding=utf-8
import random
import pymongo
import requests
from bs4 import BeautifulSoup


# 构造函数--spider1
def get_all_brand_links(start_url):
    # host网址
    host_url='https://www.guazi.com'
    # 头标签
    headers={
        'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36',
        'Connection':'keep-alive'
    }
    # 代理
    proxy_list = [
        'http://111.23.4.155：8080',
        'http://61.132.241.109:80',
        'http://122.224.227.202:3128',
        'http://183.61.236.53:3128',
        'http://101.200.143.168:80'
        ]
    # 随机获取代理ip
    proxy_ip = random.choice(proxy_list)
    proxies = {'http': proxy_ip}
    # 新建数据库
    client=pymongo.MongoClient('localhost',27017)
    guazi_web=client['guazi_web']
    brand_links=guazi_web['brand_links']
    # 发起请求
    web_data=requests.get(start_url,headers=headers,proxies=proxies)
    # 构造BeautifulSoup
    soup=BeautifulSoup(web_data.text,'lxml')
    # 取出链接
    links=soup.select('body > div.w > div.comfilter-bd > div > dl > dd > span > div > div > ul > li > div > a')
    # 存入字典
    for link in links:
        all_brand_links=host_url+link.get('href')
        # print(all_brand_links)
        # 存入数据库中
        brand_links.insert_one({'brand_link':all_brand_links})

# 爬取起始网址
start_url='http://www.guazi.com/sh/buy/'
# 调用函数
get_all_brand_links(start_url)
