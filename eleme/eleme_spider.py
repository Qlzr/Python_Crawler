# -*- coding: utf-8 -*-
"""
Created on Sun Dec 10 22:01:30 2017

@author: LZR
"""

import requests
import json

#获取通过Ajax加载的json数据
def get_json_data(offset):
    headers = {
        'Host': 'www.ele.me',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Accept-Encoding': 'gzip, deflate, br',
        'Referer': 'https://www.ele.me/place/ws1759ufjm8?latitude=23.03733&longitude=114.41837',
        'x-shard': 'loc=114.41837,23.03733',
        }
    params = {
        'extras[]':'activities',
        'geohash':'ws1759ufjm8',
        'latitude':'23.03733',
        'limit':'24',
        'longitude':'114.41837',
        'offset':str(offset),
        'terminal':'web'
        }
    url = 'https://www.ele.me/restapi/shopping/restaurants'
    try:
        r = requests.get(url, headers=headers, params=params)
        r.raise_for_status()
    except Exception as e:
        print(e)
        print("第" + str(offset) + "到" + str(offset+24) + "个数据爬取失败！")
    return r.json()

#从获取到的json数据选取想要的数据项，以列表的形式返回
def get_restaurants_info(jsons, offset):
    result = []
    for j in jsons:
        restaurant = {}
        restaurant['店铺id'] = j['id']
        restaurant['店名'] = j['name']
        restaurant['配送费'] = j['float_delivery_fee']
        restaurant['平均配送时间'] = j['order_lead_time']
        restaurant['月销量'] = j['recent_order_num']
        result.append(restaurant)
    print("第"+ str(offset+len(jsons)) +"个数据爬取完成！")
    return result
        
#将解析好的数据（列表）以json形式存储在本地 
def save_info(results):
    with open('data.json', 'w', encoding='utf-8') as file:
        file.write(json.dumps(results, indent=2, ensure_ascii=False))
    print("存储完成!")
    
if __name__=='__main__':
    results = []
    for offset in range(0, 240, 24):
        jsons = get_json_data(offset)
        results += get_restaurants_info(jsons, offset)
    save_info(results)
    