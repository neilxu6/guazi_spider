#-*-coding:utf-8-*-
import time
import random
import pymongo
import requests
from bs4 import BeautifulSoup



db_urls = [item['url'] for item in url_list.find()]
index_urls = [item['url'] for item in item_info.find()]
x = set(db_urls)
y = set(index_urls)
rest_of_urls = x-y