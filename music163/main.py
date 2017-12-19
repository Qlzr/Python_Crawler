# -*- coding: utf-8 -*-
"""
Created on Fri Dec 15 15:27:46 2017

@author: LZR
"""

from GetSingerId import Get_singer_id
from GetAlbumId import Get_album_id
from ProxyIp import Get_proxy_pool
from GetAlbumInfo import Get_album_and_aongs
from GetCommentNum import Get_comment_num
import SaveData


def all_singer_ids(url):
    '''
    爬取一个页面的歌手id
    '''
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0'}
    singer = Get_singer_id(url, headers)
    singer_ids = singer.get_singer_ids()
    return singer_ids


def all_album_ids(singer_ids):
    '''
    通过歌手id获取歌手的所有专辑号，
    爬取一个歌手页面的所有歌手的专辑号就更新一次代理ip池
    '''
    proxy_pool = get_proxy_pool()
    album = Get_album_id(singer_ids, proxy_pool)
    album_ids = album.get_album_ids()
    return album_ids


def all_albums_and_songs(album_ids):
    '''
    通过专辑号爬取专辑页面，
    将专辑信息和专辑里的所有歌曲信息存进数据库
    每爬取500张专辑更新一次代理ip池
    '''
    lenth = int(len(album_ids) / 500)
    for i in range(lenth):
        proxy_pool = get_proxy_pool()
        for album_id in album_ids[i*500: (i+1)*500]:
            album_info = Get_album_and_aongs(album_id, proxy_pool)
            signal = None
            while signal is None:
                signal = album_info.get_album_and_songs()
    proxy_pool = get_proxy_pool()
    for album_id in album_ids[lenth*500:]:
            album_info = Get_album_and_aongs(album_id, proxy_pool)
            signal = None
            while signal is None:
                signal = album_info.get_album_and_songs()
    
    
def all_comment_num():
    '''
    获取歌曲号
    通过歌曲号获取歌曲的评论数
    将评论数存进数据表song_info
    每爬取500首歌曲的评论数更新一次代理池
    '''
    song_ids = SaveData.get_song_ids()
    lenth = int(len(song_ids) / 500)
    for i in range(lenth):
        proxy_pool = get_proxy_pool()
        for song_id in song_ids[i*500: (i+1)*500]:
            com_num = Get_comment_num(song_id, proxy_pool)
            signal = None
            while signal is None:
                signal = com_num.get_comment_num()
    proxy_pool = get_proxy_pool()
    for song_id in song_ids[lenth*500:]:
        com_num = Get_comment_num(song_id, proxy_pool)
        signal = None
        while signal is None:
            signal = com_num.get_comment_num()
            
    
    

def get_proxy_pool():
    '''
    更新代理ip池
    '''
    ip_pool = Get_proxy_pool()
    proxy_pool = ip_pool.get_proxy_pool()
    return proxy_pool



if __name__ =='__main__':
    
    '''
    构建歌手页面的url,爬取所有华语男歌手的id号
    也可以将url中的id=1001换成其他的，比如修改成id=2001以爬取所有欧美男歌手id
    或者构建歌手页面的所有url爬取网易云音乐上所有歌手的id
    '''
    urls = []
    for i in range(65, 91):
        url = 'http://music.163.com/discover/artist/cat?id=1001&initial=' + str(i)
        urls.append(url)
    urls.append('http://music.163.com/discover/artist/cat?id=1001&initial=0')
    
    for url in urls:
        singer_ids = all_singer_ids(url) #获取歌手的id
        album_ids = all_album_ids(singer_ids) #获取歌手的所有专辑号
        all_albums_and_songs(album_ids) #获取专辑页面，存储专辑信息和歌曲信息
        all_comment_num()  #获取歌曲的评论数
        SaveData.close_db() #关闭数据库连接
        print('歌手页面 '+ url +'信息爬取完毕！')
    print("爬虫结束！")
    
    
    
    
    
    
        
    
    
    