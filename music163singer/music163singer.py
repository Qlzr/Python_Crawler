# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import json

def get_albums_id(singer_id):
    url = 'http://music.163.com/artist/album?id=' + str(singer_id)
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0'}
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, 'lxml')
    page_num = len(soup.find(class_='u-page').find_all('a'))-2
    albums_id = []
    for offset in range(0, 12*page_num, 12):
        url = 'http://music.163.com/artist/album?id=' + str(singer_id) + '&limit=12&offset=' + str(offset)
        r = requests.get(url, headers=headers)
        soup = BeautifulSoup(r.text, 'lxml')
        albums = soup.find(id="m-song-module").find_all('li')
        for album in albums:
            album_href = album.find(class_='msk')['href']
            albums_id.append(album_href.replace('/album?id=', ''))
    print('专辑id爬取完毕！')
    return albums_id
        
        
def get_songs_id(albums_id):
    songs_info = []
    for album_id in albums_id:
        url = 'http://music.163.com/album?id=' + album_id
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0'}
        r = requests.get(url, headers=headers)
        soup = BeautifulSoup(r.text, 'lxml')
        release_info = soup.find_all(class_='intr')
        release_time = release_info[1].get_text().split('：')[1]
        if len(release_info) == 3:
            release_company = release_info[2].get_text().split('：')[1].strip()
        else:
            release_company = '个人'
        songs_a = soup.find('ul', class_='f-hide').find_all('a')
        album_name = soup.find(class_='f-ff2').get_text()
        for song_a in songs_a:
            song_dict = {}
            song_dict['歌曲id'] = song_a['href'].replace('/song?id=', '')
            song_dict['歌曲名'] = song_a.get_text()
            song_dict['专辑id'] = album_id
            song_dict['专辑名'] = album_name
            song_dict['发行时间'] = release_time
            song_dict['发行公司'] = release_company
            songs_info.append(song_dict)
    print('歌曲信息爬取完毕！')
    return songs_info
    
def get_evalute_num(songs_info):
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
    params = {
        'csrf_token': '425ba3183ee950f06415a75625e4f3c1'
        }
    data = {
            'params':	'HoUmTNusBTh02+T3jn7N0aIXjlIDsGvtTQr/YiwePrIoKCjOZ/zldl/wZnxniTEtjgUbiGA1LJ92Hsp8WYaGlRsOR86rQVchMccG5x+7bps1UfZaQSFf2nexldh0AKWDaTf9Wa2iYB/EwwkeZN+OYSYGncVyMXqAeVtRkgLo78clkkT6KosIqLagPbnUOYNNH2AeMRXhY1Rh9LT9SJThwHFNSOlx5VioBoedr6Kyq0Q=',
            'encSecKey':	'29270ceb702cf6709a177e900d59837b2f1288c35dc9c591586cab9cac54e423bd8dedae57a082311ed0da40bd2d9732ec009808513f7a6705e57eaed1964b3a92e6d5abe2b6a9ec4caa3fd81fca9a38f80aeafd9c55c211d169b0379819734546c542c16e52f0bb53a5090651fbb8196c74a85666b30bc6a273ddbf4eef9cd5'
            }
    for song_info in songs_info:
        headers['Referer'] = 'http://music.163.com/song?id=' + song_info['歌曲id']
        url = 'http://music.163.com/weapi/v1/resource/comments/R_SO_4_' + song_info['歌曲id']
        r = requests.post(url, headers=headers, params=params, data=data)
        evalute_num = r.json()['total']
        song_info['评论数'] = evalute_num
    print('评论数爬取完毕!')
    return songs_info
    
    
def save_result(result):
    with open('data.json', 'w', encoding='utf-8') as file:
        file.write(json.dumps(result, indent=2, ensure_ascii=False))
    print("存储完成!")
    
if __name__=='__main__':
    singer_id = 3684
    albums_id = get_albums_id(singer_id)
    songs_info = get_songs_id(albums_id)
    result = get_evalute_num(songs_info)
    save_result(result)