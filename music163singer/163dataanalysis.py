#-*- coding: utf-8 -*-
"""
Created on Thu Dec  7 09:52:28 2017

@author: LZR
"""

from pandas import DataFrame
import json
import xlwt

db = json.load(open('data.json', encoding='utf-8'))

#获取歌曲评论前五的信息
col = ['歌曲名', '评论数']
top5_song = DataFrame(db, columns=col).sort_values(by=['评论数'], ascending=False)[:5]
top5_song.index = range(1,6)
top5_name = list(top5_song['歌曲名'])
top5_num = list(top5_song['评论数'])

#获取专辑评论总数前五的信息
col1 = ['专辑id', '专辑名', '评论数']
album = DataFrame(db, columns=col1)
top5_album = DataFrame(album['评论数'].groupby([album['专辑id'], album['专辑名']]).sum()).sort_values(by=['评论数'], ascending=False)[:5]
top5_album_name = list(top5_album.index)
top5_album_num = list(top5_album['评论数'].values)

#将统计的歌曲评论前五和专辑评论总数前五的信息写入Excel表格，方便画图
book = xlwt.Workbook()
sheet1 = book.add_sheet('top5_song')
sheet2 = book.add_sheet('top5_album')
sheet1.write(0, 0, '歌名')
sheet1.write(0, 1, '评论数')
sheet2.write(0, 0, '专辑名')
sheet2.write(0, 1, '评论总数')
for i in range(0, 5):
    sheet1.write(i+1, 0, top5_name[i])
    sheet1.write(i+1, 1, int(top5_num[i]))
    sheet2.write(i+1, 0, top5_album_name[i][1])
    sheet2.write(i+1, 1, int(top5_album_num[i]))
book.save('top5.xls')