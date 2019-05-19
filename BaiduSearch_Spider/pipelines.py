# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
import csv
from BaiduSearch_Spider.items import *

class BaidusearchSpiderPipeline(object):
    def process_item(self, item, spider):
        return item

class Pipeline_ToCSV(object):
    def __init__(self):
        #csv文件的位置,无需事先创建
        store_file = os.path.dirname(__file__) + '/data/baidusearch_双鸭山.csv'
        #打开(创建)文件
        self.file = open(store_file,'w',newline='',encoding='utf-8-sig') # 不带newline的话输出总会有一个空行 加入encoding='utf-8-sig'就不会乱码了
        #csv写法
        self.writer = csv.writer(self.file)
        
    def process_item(self,item,spider):
        if isinstance(item, BaidunewsSpiderItem):
            return self.process_news_item(item,spider)
        elif isinstance(item, BaidusearchSpiderItem):
            return self.process_search_item(item,spider)
        
    def process_news_item(self,item,spider):
        #判断字段值不为空再写入文件
        if item['title']!="" :
            # 组成元组：
            List=(item['title'],item['platform'],item['date'],item['time'],item['brief'],item['body'],item['link'])
            self.writer.writerow(List)
        return item
    def process_search_item(self,item,spider):
        #判断字段值不为空再写入文件
        if item['title']!="" :
            #组成元组：
            List=(item['number'],item['title'],item['time'],item['brief'],item['link'])
            self.writer.writerow(List)
        return item

    def close_spider(self,spider):
        #关闭爬虫时顺便将文件保存退出
        self.file.close()
