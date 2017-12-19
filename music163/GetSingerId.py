# -*- coding: utf-8 -*-

import requests
from lxml import etree
#import time

class Get_singer_id:
    '''
    爬取歌手列表页面，获取歌手id
    '''
    def __init__(self, url, headers):
        self.url = url
        self.headers = headers
        
    def get_singer_ids(self):
        singer_ids = []
        try:
            r = requests.get(self.url, headers=self.headers)
            r.raise_for_status()
            html = etree.HTML(r.text)
            hrefs = html.xpath("//a[@class='nm nm-icn f-thide s-fc0']/@href")
            for href in hrefs:
                singer_id = href.replace('/artist?id=', '')
                singer_ids.append(singer_id)
            print('歌手页面 '+ self.url +' 歌手id爬取成功！')
            #time.sleep(1)
        except:
            print('歌手页面 '+ self.url +' 歌手id爬取失败！')
        return singer_ids
                
            