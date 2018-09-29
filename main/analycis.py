from os import path
from wordcloud import WordCloud, ImageColorGenerator
import jieba.analyse
import matplotlib.pyplot as plt
from scipy.misc import imread
from pymongo import MongoClient
import pymongo
import os


class Analycis:
    def __init__(self):
        self.client = MongoClient('mongodb://localhost:27017/')
        self.zfdb = self.client.zfdb
        self.zfdb.authenticate("user", "password")

    # 展示条形图
    def show_line(self, title, attr, value):
        from pyecharts import Bar
        bar = Bar(title)
        bar.add("国内景点", attr, value, is_convert=False, is_label_show=True, label_text_size=18, is_random=True,
                # xaxis_interval=0, xaxis_label_textsize=9,
                legend_text_size=18, label_text_color=["#000"])
        bar.render()

    def show_data(self):
        for index in range(5):

            queryArgs = {"day_avg_pv": {"$lt": 100000}}
            rets = self.zfdb.national_month_index.find(queryArgs).sort("day_avg_pv", pymongo.DESCENDING).limit(10).skip(index*10)
            atts = []
            values = []
            file_name = "top" + str(index * 10) + "-" + str((index + 1) * 10) + ".html"
            for ret in rets:
                print(ret)
                atts.append(ret["address"])
                values.append(ret["day_avg_pv"])
            self.show_line("各景点 30 天内平均搜索量", atts, values)
            os.rename("render.html", file_name)

analyc = Analycis()
analyc.show_data()
