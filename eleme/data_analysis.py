# -*- coding: utf-8 -*-
"""
Created on Sun Dec 10 23:47:55 2017

@author: LZR
"""

from pandas import DataFrame
import json
import xlwt

db = json.load(open('data.json', encoding='utf-8'))

#获取月销量前10名的店家名字以及月销量
col1 = ['店名', '月销量']
top10_num = DataFrame(db, columns=col1).sort_values(by=['月销量'], ascending=False)[:10]
top10_name = list(top10_num['店名'])
top10_order_num= list(top10_num['月销量'])

#将获取的前十数据写进Excel表格，方便画图
book = xlwt.Workbook()
sheet1 = book.add_sheet('top10_num')
sheet1.write(0, 0, '店名')
sheet1.write(0, 1, '月销量')
for i in range(0, 10):
    sheet1.write(i+1, 0, top10_name[i])
    sheet1.write(i+1, 1, int(top10_order_num[i]))
book.save('top10.xls')