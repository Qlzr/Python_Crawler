# -*- coding: utf-8 -*-

import requests
from lxml import etree
import random

class Get_album_id:
    '''
    通过歌手id获取专辑id
    '''
    def __init__(self, singer_ids, proxy_pool):
        self.singer_ids = singer_ids
        self.proxy_pool = proxy_pool
        
    def get_album_ids(self):
        '''
        通过列表singer_ids获取所有歌手的所有专辑号，
        以列表的形式返回
        '''
        album_ids = []
        for singer_id in self.singer_ids:
            album_id = None
            while album_id is None:
                album_id = self.one_singer_album_ids(singer_id)  #如果函数返回的是None,则重新执行
            album_ids.extend(album_id)
        return album_ids
            
            
    def one_singer_album_ids(self,singer_id):
        '''
        获取一个歌手的所有专辑id
        '''
        self.singer_id = singer_id
        url = 'http://music.163.com/artist/album?id=' + self.singer_id
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0'}
        ip = random.choice(self.proxy_pool)
        proxies = {'http': ip}
        album_id = []
        try:
            r = requests.get(url, headers=headers, proxies=proxies, timeout=3)
            r.raise_for_status()
            html = etree.HTML(r.text)
            page = html.xpath("//div[@class='u-page']")       #获取歌手专辑页面的页数
            if len(page) == 0:     #如果该歌手的专辑页面只有一页，直接解析当前页面，获取专辑号
                hrefs = html.xpath("//a[@class='tit s-fc0']/@href")
                for href in hrefs:
                    _id = href.replace('/album?id=', '')    #获取当前专辑页面的所有专辑号（下同）
                    album_id.append(_id)
            else:  
                '''
                如果该歌手的专辑页面超过一页
                则执行以下程序
                '''
                page_num = len(html.xpath("//div[@class='u-page']/a")) - 2 #减去2是减去<上一页>和<下一页>这两个标签
                for offset in range(0, 12*page_num, 12):
                    url = 'http://music.163.com/artist/album?id=' + self.singer_id + '&limit=12&offset=' + str(offset)  #构建专辑页面的url
                    r = requests.get(url, headers=headers, proxies=proxies, timeout=3)
                    r.raise_for_status()
                    html = etree.HTML(r.text)
                    hrefs = html.xpath("//a[@class='tit s-fc0']/@href")
                    for href in hrefs:
                        _id = href.replace('/album?id=', '')
                        album_id.append(_id)      
            print('歌手id为'+ self.singer_id +'的专辑id爬取完毕!')
            return album_id
        except:
            print('歌手id为'+ self.singer_id +'的专辑id爬取失败!')
            print('正在重爬')
            return None     #爬取失败了就返回None
            
            