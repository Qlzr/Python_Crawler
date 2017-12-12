# -*- coding: utf-8 -*-
"""
Created on Tue Dec 12 10:10:46 2017

@author: LZR
"""

import requests
from lxml import etree
import threading  #多线程处理与控制
import time

base_url = 'http://www.xicidaili.com/wt/'
headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0'
        }

#获取代理ip的网页
def get_html(url):
    r = requests.get(url, headers=headers)
    r.raise_for_status()
    html = r.text
    return html

#解析网页，获取代理的ip地址和端口，并以列表的形式返回
def html_parser(html):
    result = []
    html = etree.HTML(html)
    ip_info = html.xpath('//table[@id="ip_list"]/tr')
    del ip_info[0]
    for ip in ip_info:
        res = 'http://' + ip.xpath('td[2]/text()')[0] + ':' + ip.xpath('td[3]/text()')[0]
        result.append(res)
    return result

#测试代理，并将可用的代理以列表的形式返回
def get_use_proxy(ip):
    proxies = {'http': ip}
    try:
        print('正在测试代理ip：' + ip +'\n')
        r = requests.get('http://www.baidu.com', proxies=proxies, timeout=3)
        if r.status_code == 200:
            print('代理ip：' + ip + '有效可用' + '\n')
            save_good_ip(ip) #将测试有效可用的代理ip写入txt文本中
    except:
        pass

#启动多线程测试ip地址的可用性
def start_test_ip(results):
    for ip in results:
        th=threading.Thread(target=get_use_proxy,args=(ip,))
        th.start() #启动线程
    
#将爬取到的代理ip写入txt文本中
def save_all_ip(all_ip):
    with open('all_ip.txt', 'w') as file:
        for ip in all_ip:
            file.write(ip + '\n')
        print('代理ip写入完毕!')
    #先清空上一次爬取后的可用ip
    with open('good_ip.txt', 'w') as f:
        f.write('')


#将可用的代理ip以追加的形式写入txt文本中
def save_good_ip(ip):
    with open('good_ip.txt', 'a') as file:
        file.write(ip + '\n')
 
    
if __name__ == '__main__':
    results = []
    page = 6 #爬取的页数
    for i in range(0, page):
        url = base_url + str(i+1)
        html = get_html(url)
        result = html_parser(html)
        results.extend(result)
    save_all_ip(results)
    start_test_ip(results)
    time.sleep(2)
    print("可用ip存储完毕！")
    