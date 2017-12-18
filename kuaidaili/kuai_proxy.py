# -*- coding: utf-8 -*-
"""
Created on Wed Dec 13 13:46:00 2017

@author: LZR
"""

import requests
import time
from lxml import etree
import threading

#获取HTML页面
def get_html(url):
    headers = {
            'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0'
            }
    try:
        r = requests.get(url, headers=headers)
        r.raise_for_status()
        html = r.text
        return html
    except Exception as e:
        print("第" + str(i+1) +"页爬取失败，失败原因：")
        print(e)

#解析html页面，获取ip地址和端口号    
def get_ip(html):
    page_ip = []
    html = etree.HTML(html)
    ips = html.xpath('//tbody/tr')
    for ip in ips:
        proxy_ip = "http://" + ip.xpath('td[@data-title="IP"]/text()')[0] + ":" + ip.xpath('td[@data-title="PORT"]/text()')[0]
        page_ip.append(proxy_ip)
    return page_ip

#保存爬取到的ip，并清空上次爬取的可用的ip    
def save_all_ip(all_ip):
    with open('all_ip.txt', 'w') as file:
        for ip in all_ip:
            file.write(ip + '\n')
    print('所有ip保存完毕')
            
    with open('good_ip.txt', 'w') as f:
        f.write('')

#启动多线程        
def start_test_ip(all_ip):
    for ip in all_ip:
        th = threading.Thread(target=get_good_ip, args=(ip,)) 
        th.start()

#测试代理ip的可用性        
def get_good_ip(ip):
    proxies = {'http': ip}
    try:
        print('正在测试代理ip：' + ip +'\n')
        r = requests.get('http://www.baidu.com', proxies=proxies, timeout=3)
        if r.status_code == 200:
            print('代理ip：' + ip + '有效可用' + '\n')
            save_good_ip(ip) 
    except:
        pass

#将测试有效可用的代理ip写入txt文本中    
def save_good_ip(ip):
    with open('good_ip.txt', 'a') as file:
        file.write(ip + '\n')
 

if __name__ == '__main__':
    base_url = "http://www.kuaidaili.com/free/intr/"   #普通ip
    #base_url = "http://www.kuaidaili.com/free/inha/"  #高匿ip
    all_ip =[]
    page = 6
    for i in range(0, page):
        url = base_url + str(i+1)
        html = get_html(url)
        time.sleep(1)
        page_ip = get_ip(html)
        all_ip.extend(page_ip)
    print(str(page)+'页的代理ip爬取完成')
    save_all_ip(all_ip)
    start_test_ip(all_ip)
    time.sleep(3)
    print('爬取结束！')