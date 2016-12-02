#-*-coding:utf-8-*-
from multiprocessing import Pool
from second_get_every_brand_car_links import get_more_cars_detail

get_more_cars_detail()
print('======所有的工作已经完毕~======')
# if __name__ == '__main__':
#     pool=Pool()
#     pool.apply(get_more_cars_detail())
#     pool.close()
#     pool.join()
#     print('======所有的工作已经完毕~======')