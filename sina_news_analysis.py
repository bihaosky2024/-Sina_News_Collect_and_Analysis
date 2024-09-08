import pandas as pd
from wordcloud import WordCloud
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams['font.family'] = ['SimHei']
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
import jieba
import os
from sqlalchemy import create_engine

from parameter import user, password, host, port, font_path


class NewsDataAnalysis:
    def __init__(self, database, news_type, table, fig_dir, color):
        self.database = database
        self.news_type = news_type
        self.table = table
        self.fig_dir = fig_dir
        self.color = color

    def sql_to_df(self, user, password, host, port):
        engine = create_engine(f'mysql+pymysql://{user}:{password}@{host}:{port}/{self.database}')
        self.df = pd.read_sql_table(self.table, engine)

    @staticmethod
    def _time_classification(time_str):
        hour, minute = time_str.split(':')
        hour, minute = int(hour), int(minute)
        if 0 <= minute <= 30:
            pass
        else:
            hour += 1
        if hour == 24:
            hour = 0
        minute = 0
        return str(hour).zfill(2) + ':' + str(minute).zfill(2)

    def clean_data(self):
        # 将空字符串替换为NaN
        self.df.replace('', np.nan, inplace=True)
        self.df.drop_duplicates(keep='first', inplace=True)
        self.df.dropna(axis=0, how='any', inplace=True)
        self.df[['date', 'time']] = self.df['release_time'].str.split(pat=' ', expand=True)
        self.df.drop('release_time', axis=1, inplace=True)
        # 将日期格式转换为“YYYY-MM-DD”
        self.df['date'] = self.df['date'].str.replace('年', '-').str.replace('月', '-').str.replace('日', '')
        # 将字符串转换为日期格式
        self.df['date'] = pd.to_datetime(self.df['date'])
        # 提取日期部分（去掉时分秒）
        self.df['date'] = self.df['date'].dt.date
        # 将时间格式转换为“HH:00”
        self.df['time'] = self.df['time'].apply(self._time_classification)

    def create_word_ls(self):
        word_ls = []
        for i in range(self.df.shape[0]):
            word_ls.extend(jieba.lcut(self.df.iloc[i, 1]))
        self.title_words = ' '.join(word_ls)

    def read_cn_stopwords(self):
        with open('./stopwords/cn_stopwords.txt', 'r', encoding='utf-8') as f:
            self.stopwords = set(f.read().splitlines())

    def source_frequency(self):
        fig_name = 'news_source_frequency.png'
        if not os.path.exists(self.fig_dir):
            os.makedirs(self.fig_dir)

        source_counts = self.df['source'].value_counts()

        plt.figure(figsize=(12, 9), dpi=300)
        source_counts[:10].plot.bar(color=self.color)
        plt.title(f'Frequency of {self.news_type} Source: Top 10', fontsize=18, fontweight='bold', y=1.03)
        plt.xticks(rotation=45, fontsize=12)  # 设置为45度旋转
        plt.yticks(range(0, 201, 25), fontsize=12)
        plt.xlabel('News Source', fontsize=16, fontweight='bold')
        plt.ylabel('Frequency', fontsize=16, fontweight='bold', labelpad=15)
        plt.tight_layout() # 调整布局
        plt.savefig(self.fig_dir + fig_name, dpi=300)
        plt.close()

    def date_frequency(self):
        fig_name = 'news_date_frequency.png'
        date_counts = self.df['date'].value_counts()
        # 按日期排序
        date_counts.sort_index(inplace=True)

        plt.figure(figsize=(12, 9), dpi=300)
        date_counts.plot.bar(color=self.color)
        plt.title(f'Amount of Daily News: {self.news_type} ', fontsize=18, fontweight='bold', y=1.02)
        plt.xticks(rotation=45, fontsize=11)  # 设置为45度旋转
        plt.yticks(range(0, 40, 5), fontsize=12)
        plt.xlabel('Date', fontsize=16, fontweight='bold', labelpad=10)
        plt.ylabel('Amount of News', fontsize=16, fontweight='bold', labelpad=10)
        plt.tight_layout() # 调整布局
        # 确保不调用 plt.legend() 或禁用它
        plt.legend().set_visible(False)
        plt.savefig(self.fig_dir + fig_name, dpi=300)
        plt.close()

    def time_frequency(self):
        fig_name = 'news_hours_frequency.png'
        time_counts = self.df['time'].value_counts()
        time_counts.sort_index(inplace=True)
        time_counts.plot.bar(color=self.color)
        plt.title(f'Frequency of {self.news_type} in Hours', fontsize=10, fontweight='bold', y=1.03)
        plt.xticks(rotation=45, fontsize=7)
        plt.yticks(range(0, 50, 10), fontsize=7)
        plt.xlabel('Hours', fontsize=9, fontweight='bold')
        plt.ylabel('Frequency', fontsize=9, fontweight='bold', labelpad=15)
        plt.tight_layout()
        plt.savefig(self.fig_dir + fig_name, dpi=300)
        plt.close()

    def word_cloud(self):
        fig_name = 'title_word_cloud.png'
        # 设置词云形状的图片
        mask_file = './word_cloud_image/cat.png'
        mask = Image.open(mask_file)
        mask = np.array(mask)
        width, height = mask.shape[:2]

        # 创建词云对象
        wc = WordCloud(width=width, height=height, background_color="white", font_path=font_path, mask=mask
                       , stopwords=self.stopwords)
        wc.generate(self.title_words)
        # 显示词云
        plt.figure(figsize=(8, 6))
        plt.imshow(wc, interpolation='bilinear')
        plt.axis("off")
        plt.savefig(self.fig_dir + fig_name)
        plt.close()


    def main(self):
        print(f'Start {self.news_type} data analysis.')
        self.sql_to_df(user, password, host, port)
        self.clean_data()
        print(f'There are {self.df.shape[0]} pieces of {self.news_type}.')
        print(f'Columns: {self.df.columns}')
        self.create_word_ls()
        self.read_cn_stopwords()
        self.source_frequency()
        print(f'Source frequency analysis of {self.news_type} saved in {self.fig_dir}.')
        self.date_frequency()
        print(f'Date frequency analysis of {self.news_type} saved in {self.fig_dir}.')
        self.time_frequency()
        print(f'Time frequency analysis of {self.news_type} saved in {self.fig_dir}.')
        self.word_cloud()
        print(f'Word cloud analysis of {self.news_type} title saved in {self.fig_dir}.')
        print(f'Finish {self.news_type} data analysis.' + '\n')


if __name__ == '__main__':
    main_news = NewsDataAnalysis(database='sina_test', news_type='Main News', table='daily_main_news'
                                 , fig_dir='./main_news_pic/', color='pink')
    main_news.main()

    domestic_news = NewsDataAnalysis(database='sina_test', news_type='Domestic News', table='domestic_news'
                                 , fig_dir='./domestic_news_pic/', color='pink')
    domestic_news.main()

    inter_news = NewsDataAnalysis(database='sina_test', news_type='International News', table='inter_news'
                                 , fig_dir='./inter_news_pic/', color='lightblue')
    inter_news.main()