# -*- coding: utf-8 -*-
import scrapy
import urllib
from dangdang_spider.items import DangdangSpiderItem

class SpiderSpider(scrapy.Spider):
    name = "spider"
    
    #先清空上一次爬取的数据
    with open('data.json', 'w') as f:
        f.write('')
    
    #输入要爬取的商品名字
    data = input('请输入你要爬取的商品：')
    
    #将输入的商品名称进行url编码
    data = urllib.parse.quote(data)
    start_urls = ['http://search.dangdang.com/?key='+ data +'&act=input&page_index=1']
    page_urls = []
    
    def parse(self, response):
        
        #获取商品总数
        counts = response.xpath("//span[@class='sp total']/em/text()").extract()[0]
        
        #计算出要爬取的商品页数
        pages = int(int(counts)/60 + 1 )
        
        #构建每一页的url
        for page in range(pages):
            page_url = 'http://search.dangdang.com/?key='+ self.data +'&act=input&page_index=' + str(page+1)
            self.page_urls.append(page_url)
        
        #利用每一页的url，调用get_product_info函数，爬取商品信息
        for page_url in self.page_urls:
            yield scrapy.Request(page_url, callback=self.get_product_info)
            
    def get_product_info(self, response):
        '''
        获取商品名、商品价格、商品链接、评论数、以及店家名称
        '''
        items = []
        lenth = len(response.xpath("//div[@dd_name='普通商品区域']/ul/li/a/@title").extract())
        for i in range(lenth):
            item = DangdangSpiderItem()
            item['product_name'] = response.xpath("//div[@dd_name='普通商品区域']/ul/li/a/@title").extract()[i]
            item['product_price'] = response.xpath("//div[@dd_name='普通商品区域']/ul/li/p[@class='price']/span[1]/text()").extract()[i]
            item['product_url'] = response.xpath("//div[@dd_name='普通商品区域']/ul/li/a/@href").extract()[i]
            item['comment_num'] = response.xpath("//a[@dd_name='单品评论']/text()").extract()[i]
            if response.xpath("//div[@dd_name='普通商品区域']/ul/li["+ str(i+1) +"]//a[@dd_name='单品店铺']/text()").extract() == []:
                item['stroe'] = '当当自营'
            else:
                item['stroe'] = response.xpath("//div[@dd_name='普通商品区域']/ul/li["+ str(i+1) +"]//a[@dd_name='单品店铺']/text()").extract()[0]
            items.append(item)
        
        return items
