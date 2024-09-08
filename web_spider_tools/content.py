# ContentSinglePage:专用于解析提取一张网页的信息
# ContentMultiPages:专用于解析提取多张网页(一张主页面，及多张由主页面链出的多张子页面)的信息
# ContentPicture:专用于解析提取多张网页(一张主页面，及多张由主页面链出的多张子页面)及图片的信息

import pandas as pd
import sqlalchemy
from concurrent.futures import ThreadPoolExecutor
import os
from .crawl import get_content


class ContentSinglePage:
    def __init__(self):
        pass

    def print(self):
        attr_ls = list(vars(self))
        length = len(getattr(self, attr_ls[0]))
        for i in range(length):
            for attr in attr_ls:
                print(f'{attr}:')
                print(getattr(self, attr)[i])
            print('\n')

    def to_txt(self, txt_file):
        attr_ls = list(vars(self))
        length = len(getattr(self, attr_ls[0]))
        for i in range(length):
            for attr in attr_ls:
                with open(txt_file, 'a', encoding='utf-8') as f:
                    f.write(f'{attr}:\n')
                    f.write(f'{getattr(self, attr)[i]}\n')
            with open(txt_file, 'a', encoding='utf-8') as f:
                f.write('\n')

    def to_excel(self, excel_file):
        df = pd.DataFrame({key: getattr(self, key) for key in vars(self)})
        df.to_excel(excel_file, index=False)

    def to_mysql(self, database, table, user, password, host, port):
        # need to create a new database at first.
        # if_exists='append', means the old data will not be removed.
        engine = sqlalchemy.create_engine(f'mysql+pymysql://{user}:{password}@{host}:{port}/{database}')
        df = pd.DataFrame({key: getattr(self, key) for key in vars(self)})
        df.to_sql(table, engine, if_exists='append', index=False)


class ContentMultiPages(ContentSinglePage):
    def __init__(self, url, title):
        super().__init__()
        self.url = url
        self.title = title

    def print_latest(self):
        attr_ls = list(vars(self))
        length = len(getattr(self, attr_ls[-1]))
        for attr in attr_ls:
            print(f'{attr}:')
            print(getattr(self, attr)[length-1])
        print('\n')


class ContentPicture(ContentMultiPages):
    def __init__(self, url, title, picture):
        super().__init__(url, title)
        self.picture = picture

    def save_picture(self, pic_dir, max_workers=5):
        if not os.path.exists(pic_dir):
            os.makedirs(pic_dir)

        # 使用 ThreadPoolExecutor 并发下载图片
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            for picture, title in zip(self.picture, self.title):
                executor.submit(self._download_picture, picture, title, pic_dir)

    @staticmethod
    def _download_picture(picture, title, pic_dir):
        pic_name = '_'.join(title[:20].split(' ')) + '.jpg'
        pic_file = os.path.join(pic_dir, pic_name)
        with open(pic_file, 'wb') as f:
            pic_content = get_content(picture)
            if pic_content is not None:
                f.write(pic_content)
                print(f"{picture} download successfully")
            else:
                print(f"{picture} download unsuccessfully")
