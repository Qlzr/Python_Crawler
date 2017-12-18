# -*- coding: utf-8 -*-

import requests
from lxml import etree
import threading  #多线程处理与控制
import time

class Get_proxy_pool:
    def get_proxy_pool(self):
        '''
        获取西刺代理网站上的代理ip
        将测试可用的ip保存在txt文本中
        同时以列表的形式将可用的ip返回去
        '''
        base_url = 'http://www.xicidaili.com/wt/'
        headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0'}
        results = []
        page = 6
        
        '''先清空上一次爬取后的可用ip'''
        with open('good_ip.txt', 'w') as f:
            f.write('')
        for i in range(0, page):
            url = base_url + str(i+1)
            html = self.get_html(url, headers)
            result = self.html_parser(html)
            results.extend(result)
        proxy_pool = self.start_test_ip(results)
        print('代理池已更新！')
        return proxy_pool
            
            
            
    def get_html(self, url, headers):
        self.url = url
        self.headers = headers
        r = requests.get(self.url, headers=self.headers)
        r.raise_for_status()
        html = r.text
        return html
        
    def html_parser(self,html):
        '''解析页面，获取当前页面的所有代理ip'''
        result = []
        self.html = etree.HTML(html)
        ip_info = self.html.xpath('//table[@id="ip_list"]/tr')
        del ip_info[0]
        for ip in ip_info:
            res = 'http://' + ip.xpath('td[2]/text()')[0] + ':' + ip.xpath('td[3]/text()')[0]
            result.append(res)
        return result  

    def start_test_ip(self, results):
        '''启动多线程测试ip地址的可用性'''
        ths = []
        for ip in results:
            th=threading.Thread(target=self.get_use_proxy,args=(ip,))
            th.start() #启动线程
            ths.append(th)
        for th in ths:
            th.join()
        time.sleep(3)
        with open('good_ip.txt', 'r') as file:
            proxy_pool = file.read().split('\n')
            del proxy_pool[-1]
        return proxy_pool

    def get_use_proxy(self,ip):
        '''通过ip代理的方式请求百度首页，以测试ip的可用性'''
        proxies = {'http': ip}
        try:
            r = requests.get('http://www.baidu.com', proxies=proxies, timeout=3)
            if r.status_code == 200:
                self.save_good_ip(ip) #将测试有效可用的代理ip写入txt文本中
        except:
            pass #将不可用的ip丢弃掉
        
    def save_good_ip(self,ip):
        '''将可用的代理ip以追加的形式写入txt文本中'''
        with open('good_ip.txt', 'a') as file:
            file.write(ip + "\n" )
            