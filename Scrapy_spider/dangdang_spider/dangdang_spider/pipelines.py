# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json

class DangdangSpiderPipeline(object):
    def process_item(self, item, spider):
        
        #将爬取的到的每一条商品信息以追加的形式存储在json文件中
        with open('data.json', 'a', encoding='utf-8') as file:
            file.write(json.dumps(dict(item), indent=2, ensure_ascii=False))
        
        return item
