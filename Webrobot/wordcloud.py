#PythonFileForTest

import wordcloud
import jieba
from scipy.misc import imread

f = open('test.txt', 'r', encoding = 'gbk')
t = f.read()
f.close()
ls = jieba.lcut(t)
txt = ' '.join(ls)

mk = imread('template.png')
w = wordcloud.WordCloud( font_path = 'msyh.ttc', \
    width = 1000, height = 700, background_color = 'white', \
    mask = mk )
w.generate(txt)
w.to_file('test2.png')