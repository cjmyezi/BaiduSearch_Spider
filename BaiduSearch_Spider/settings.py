# -*- coding: utf-8 -*-

# Scrapy settings for BaiduSearch_Spider project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'BaiduSearch_Spider'   

SPIDER_MODULES = ['BaiduSearch_Spider.spiders']
NEWSPIDER_MODULE = 'BaiduSearch_Spider.spiders'

ROBOTSTXT_OBEY = False
# headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'}
DOWNLOADER_MIDDLEWARES = {
    'BaiduSearch_Spider.customUserAgent.RandomUserAgent':300,
     # 禁用内置的中间件，启用自定义
    'BaiduSearch_Spider.middlewares.BaidusearchSpiderDownloaderMiddleware': None,
    'scrapy.downloadermiddleware.useragent.UserAgentMiddleware': None,
}

ITEM_PIPELINES = {
    'BaiduSearch_Spider.pipelines.Pipeline_ToCSV':100,
}

DOWNLOAD_TIMEOUT = 300 # 下载网页超时时间
