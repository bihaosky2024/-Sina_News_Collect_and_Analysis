from web_spider_tools.content import ContentMultiPages
from web_spider_tools.crawl import *
from parameter import user, password, host, port

import os
import datetime
import time


class ShortNews(ContentMultiPages):
    def __init__(self, url, title, release_time, source):
        super().__init__(url, title)
        self.release_time = release_time
        self.source = source

    def parse_main_page(self, url_0, selector_0):
        html = get_html(url_0)
        for tag in select_tag_ls(html, selector_0):
            self.url.append(tag['href'])
            self.title.append(tag.text)

    def parse_news(self, selector_1, selector_2):
        for url in self.url:
            html = get_html(url)
            self.release_time.append(select_tag_text(html, selector_1))
            self.source.append(select_tag_text(html, selector_2))
            self.print_latest()
            time.sleep(2)


class LongNews(ShortNews):
    def __init__(self, url, title, release_time, source, content):
        super().__init__(url, title, release_time, source)
        self.content = content

    def parse_news_content(self, selector_1, selector_2, selector_3):
        for url in self.url:
            html = get_html(url)
            self.release_time.append(select_tag_text(html, selector_1))
            self.source.append(select_tag_text(html, selector_2))
            self.content.append('\n'.join(select_tag_text_ls(html, selector_3)))
            self.print_latest()
            time.sleep(5)


def get_short_news(selector_ls, table):
    url = 'https://news.sina.com.cn/'
    database = 'sina_test'
    short_news = ShortNews([], [], [], [])
    selector_0, selector_1, selector_2 = selector_ls
    short_news.parse_main_page(url, selector_0)
    short_news.parse_news(selector_1, selector_2)
    short_news.to_mysql(database, table, user, password, host, port)


def get_long_news(selector_ls, news_dir, news_kind):
    url = 'https://news.sina.com.cn/'
    long_news = LongNews([], [], [], [], [])
    selector_0, selector_1, selector_2, selector_3 = selector_ls
    long_news.parse_main_page(url, selector_0)
    long_news.parse_news_content(selector_1, selector_2, selector_3)

    if not os.path.exists(news_dir):
        os.mkdir(news_dir)
    news_file = os.path.join(news_dir, f'{news_kind}_{datetime.date.today()}.txt')
    long_news.to_txt(news_file)


if __name__ == '__main__':
    # daily main news
    get_short_news(['h1[data-client] a', 'span.date', 'a.source'], 'daily_main_news')
    get_long_news(['h1[data-client] a', 'span.date', 'a.source', 'div.article p'], './main_news', 'Main_news')
    # domestic news
    get_short_news(['ul#blk_gnxw_011 > li > a', 'span.date', '.source'], 'domestic_news')
    get_long_news(['ul#blk_gnxw_011 > li > a', 'span.date', '.source', 'div.article p'], './domestic_news', 'Domestic_news')
    # international news
    get_short_news(['ul#blk_gjxw_011 > li > a', 'span.date', '.source'], 'inter_news')
    get_long_news(['ul#blk_gjxw_011 > li > a', 'span.date', '.source', 'div.article p'], './inter_news', 'inter_news')
