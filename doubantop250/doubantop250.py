# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import json


def get_html(url):  #爬取每一页HTML页面的源代码
    try:
        response = requests.get(url, headers=headers)
        html = response.text
        return html
    except:
        print("豆瓣电影top250第" + str((int(offset) + 25) / 25) + "页爬取失败")
    
def parser_html(html):   #对爬取到的HTML页面进行解析并获取信息
    soup = BeautifulSoup(html, 'lxml')
    movie_info = []
    items = soup.find_all(class_='item')
    for item in items:
        item_dict = {}
        
        #获取节点信息
        order = item.find(name='em').get_text() #获取排名
        name = item.find_all(class_='title') #获取中文影名和外文影名
        other_name = item.find(class_='other').get_text() #获取影片别名
        info = item.find(name='p', class_='').get_text().strip().split('\n') #获取影片信息（导演、年份、地区、类型）
        evaluate_info= item.find(class_='star').find_all(name='span') #获取评价信息
        grade = evaluate_info[1].get_text()  #获取评分
        evaluate_num = evaluate_info[3].get_text()[:-3] #获取评价人数
        quote = item.find(class_="inq").get_text() #获取语录
        
        
        item_dict["排名"] = order
        item_dict["影名"] = name[0].get_text()
        if len(name) == 2:
            item_dict["外文名"] = name[1].get_text().split('\xa0')[2]
        item_dict["别名"] = other_name.split('\xa0')[2]
        item_dict["导演"] = info[0].split('\xa0\xa0\xa0')[0].split(':')[1]
        item_dict["年份"] = info[1].strip().split('\xa0/\xa0')[0]
        item_dict["地区"] = info[1].strip().split('\xa0/\xa0')[1]
        item_dict["类型"] = info[1].strip().split('\xa0/\xa0')[2]
        item_dict["评分"] = grade
        item_dict["评价人数"] = evaluate_num
        item_dict["语录"] = quote
        
        movie_info.append(item_dict)
    print("豆瓣电影top250第" + str(int(offset+25) / 25) + "页完成爬取")
    return movie_info

def save_file(movie_info):  #存储获取到的信息
    with open('data.json', 'w', encoding='utf-8') as file:
        file.write(json.dumps(movie_info, indent=2, ensure_ascii=False))
    print("存储完成")
   
    
if __name__ == '__main__':
    headers = {
               'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0'
               }
    movie_info = []
    for offset in range(0, 250, 25):
        url = 'https://movie.douban.com/top250?start=' + str(offset) + '&filter='
        html = get_html(url)
        movie_info = movie_info + parser_html(html)
    save_file(movie_info)