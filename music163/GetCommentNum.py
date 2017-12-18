# -*- coding: utf-8 -*-

import requests
import random
import SaveData

class Get_comment_num:
    '''
    通过歌曲号获取评论数
    '''
    def __init__(self, song_id, proxy_pool):
        self.song_id = song_id
        self.proxy_pool = proxy_pool
        
    def get_comment_num(self):
        '''
        通过歌曲号获取歌曲的评论数
        并将评论数存进数据表song_info中
        '''
        headers = {
            'Host': 'music.163.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0',
            'Accept': '*/*',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Accept-Encoding': 'gzip, deflate',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Content-Length': '526',
            'Cookie': 'JSESSIONID-WYYY=km3Kc9Fov%2FxcFuB47%2BSw%2FfgOt1e5zB3%2BA7aRi8OPOn%2Fl%2B%5CFoKVjoyzMPiY0udXp4Bu3X8g6o%2Fm%2B8QpP9EeQEAdaxg2Sint4ReA85VfJkvhCP4QmzD8iyQkSYlNtFcazFMtQKolBXgk8MKQMmSAK1fN4ikUCNacOD30IAgwaqHi%2BgWWsC%3A1512578229729; _iuqxldmzr_=32; _ntes_nnid=c34ac6104bdc42af2c7b93c33ec7269a,1508943621025; _ntes_nuid=c34ac6104bdc42af2c7b93c33ec7269a; __utma=94650624.1549906697.1508943622.1512564249.1512571977.13; __utmz=94650624.1512552564.11.4.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __utmc=94650624; __csrf=425ba3183ee950f06415a75625e4f3c1; playerid=89965856; __utmb=94650624.20.10.1512571977',
            'Connection': 'keep-alive'
            }
        params = {'csrf_token': '425ba3183ee950f06415a75625e4f3c1'}
        data = {
            'params':	'HoUmTNusBTh02+T3jn7N0aIXjlIDsGvtTQr/YiwePrIoKCjOZ/zldl/wZnxniTEtjgUbiGA1LJ92Hsp8WYaGlRsOR86rQVchMccG5x+7bps1UfZaQSFf2nexldh0AKWDaTf9Wa2iYB/EwwkeZN+OYSYGncVyMXqAeVtRkgLo78clkkT6KosIqLagPbnUOYNNH2AeMRXhY1Rh9LT9SJThwHFNSOlx5VioBoedr6Kyq0Q=',
            'encSecKey':	'29270ceb702cf6709a177e900d59837b2f1288c35dc9c591586cab9cac54e423bd8dedae57a082311ed0da40bd2d9732ec009808513f7a6705e57eaed1964b3a92e6d5abe2b6a9ec4caa3fd81fca9a38f80aeafd9c55c211d169b0379819734546c542c16e52f0bb53a5090651fbb8196c74a85666b30bc6a273ddbf4eef9cd5'
            }
        headers['Referer'] = 'http://music.163.com/song?id=' + self.song_id
        url = 'http://music.163.com/weapi/v1/resource/comments/R_SO_4_' + self.song_id
        ip = random.choice(self.proxy_pool)
        proxies = {'http': ip}
        
        try:
            r = requests.post(url, headers=headers, params=params, data=data, proxies=proxies, timeout=3)
            r.raise_for_status()
            comment_num = r.json()['total']  #请求的响应结果是json文件
            SaveData.save_comment_num(comment_num, self.song_id)  #调用函数，将评论数保存到数据表song_info中
            print('歌曲id为' + self.song_id + '的评论数爬取成功！')
            return 1
        except:
            print('歌曲id为' + self.song_id + '的评论数爬取失败！')
            print('正在重爬')
            return None
        