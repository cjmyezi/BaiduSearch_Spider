# 用来body正文部分可能属于的路径
# 使用的时候可以自己分析网页的html修改或者增添列表
path_list = [
    '//div[@id="p-detail" ]', # 新华网
    '//div[@class="post_body" ]',#网易新闻
    '//div[@class="box_con" ]',# 人民网
    '//div[@class="news_show_cont" ]',#东方新闻网
    '//div[@class="display-content" ]',# 搜狐新闻
    '//div[@class="inner" ]',# 参考消息
    '//div[@class="content all-txt" ]',# 观察者新闻
    '//div[@class="news-content" ]',# 上观新闻
    '//div[@class="article-body" ]',# 网易新闻
    '//div[@class="article" ]',
    '//div[@class="content"]',
    '//div[@class="show_text"]',
    '//div[@class="details_box"]',
    '//article',
    '//v_news_content',

]