# Sina_News_Collect_and_Analysis

## 项目介绍

在本项目中，我分别收集了发布于新浪网站的国内（Domestic News）与国际新闻（International News）。针对每条新闻，我都一一记录了新闻的标题，发布时间，来源及新闻报道的正文，并将相关数据存储于MySQL数据库中，以供后期数据查询与分析。之后依据收集到的新闻数据，进行数据格式清洗，冗余数据剔除等数据预处理步骤。接下来分析了新闻发布日期、发布时刻、新闻来源的分布情况，最后制作了新闻标题的词云分布图。通过对比国内与国际新闻分布情况的差异，分析隐藏在数据背后的统计规律与现象。

## 第三方依赖库

- requests
- bs4
- lxml
- re
- selenium
- pandas
- matplotlib
- pillow
- jieba
- wordcloud
- sqlalchemy

## 使用方法

第一步，安装第三方依赖库

第二步，下载并配置mysql数据库连接信息

第三步，修改parameter.py文件，设置mysql数据库连接及字体文件路径参数

第四步，采集新闻数据，运行爬虫脚本sina_news_spider.py

第五步，完成数据采集之后，运行数据分析脚本sina_news_analysis.py

项目预期达成效果可见于微信推送：https://mp.weixin.qq.com/s?__biz=MzIwNjY0MTIwNA==&mid=2247484102&idx=1&sn=99c1723f1d6c5aa6b43c58591df5a330&chksm=971fc39da0684a8b16ccfb36d5d7b38aec64d11d83666ab5ea7f94bef61d03834dbcca3d5767&token=502482994&lang=zh_CN#rd



