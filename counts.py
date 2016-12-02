#-*-coding:utf-8-*-
import time
import pymongo

client = pymongo.MongoClient('localhost', 27017)
guazi_web = client['guazi_web']
brand_links = guazi_web['brand_links']
cars_info = guazi_web['cars_info']

while True:
    print(cars_info.find().count())
    time.sleep(8)