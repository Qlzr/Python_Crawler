# -*- coding: utf-8 -*-

import requests
from lxml import etree
import SaveData
import random

class Get_album_and_aongs:
    '''
    通过专辑号获取专辑信息和歌曲信息
    '''
    def __init__(self, album_id, proxy_pool):
        self.album_id = album_id
        self.proxy_pool = proxy_pool
        
    def get_album_and_songs(self):
        '''
        该函数用于通过专辑号获取专辑信息
        以及该专辑包含的所有歌曲信息
        将获取的信息保存到数据库
        '''
        url = 'http://music.163.com/album?id=' + self.album_id
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0'}
        ip = random.choice(self.proxy_pool)
        proxies = {'http': ip}
        try:
            r = requests.get(url, headers=headers, proxies=proxies, timeout=3) #请求一张专辑的歌曲列表页面
            r.raise_for_status()
            html = etree.HTML(r.text)
            
            '''解析获取专辑信息，包括专辑号、专辑名、歌手号、歌手名、发行时间和发行单位'''
            album_info = {} 
            album_info['album_id'] = self.album_id
            album_info['album_name'] = html.xpath("//h2[@class='f-ff2']/text()")
            album_info['singer_id'] = html.xpath("//p[@class='intr']//a/@href")[0].replace('/artist?id=', '')
            album_info['singer_name'] = html.xpath("//p[@class='intr']//a/text()")
            album_info['release_time'] = html.xpath("//p[@class='intr']/text()")[0]
            if len(html.xpath("//p[@class='intr']/text()")) > 1:
                album_info['release_company'] = html.xpath("//p[@class='intr']/text()")[1].strip()
            else:    
                album_info['release_company'] = '无'  #有些专辑没有标明发行单位，此类统统用‘无’表示
            
            '''解析获取一张专辑的所有歌曲信息'''    
            songs_info = [] 
            for i in range(len(html.xpath("//ul[@class='f-hide']/li"))):
                '''解析获取一首歌的信息，包括歌曲号、歌曲名、所属专辑号、所属专辑名'''
                song_info = {}  
                song_info['song_id'] = html.xpath("//ul[@class='f-hide']/li/a/@href")[i].replace('/song?id=', '')
                song_info['song_name'] = html.xpath("//ul[@class='f-hide']/li/a/text()")[i]
                song_info['album_id'] = album_info['album_id']
                song_info['album_name'] = album_info['album_name']
                songs_info.append(song_info)
            
            '''调用函数，保存专辑信息和歌曲信息到数据库'''
            SaveData.save_album_info(album_info)
            SaveData.save_songs_info(songs_info)
            
            print("专辑id为"+ self.album_id +"的信息获取完毕")
            return 1
        except:
            print("专辑id为"+ self.album_id +"的信息获取失败")
            print("正在重新获取")
            return None
        