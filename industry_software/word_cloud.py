from os import path
#用来做词云图的模块
from PIL import Image
import re
import jieba
from jieba import analyse
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import numpy as np

# 查看并生成词语图
d = path.dirname(__file__)
stopwords = {}  # 定义停词表
freq = {"word":[],"nums":[]} # 常用词列
#生成停词表
def stopword(textpath):
    global stopwords
    fl = open(path.join(textpath , 'stopwords.txt'),'r' ,encoding="utf-8")
    for line in fl.readlines():
        stopwords.setdefault(line.strip(), 0)
        stopwords[line.strip()] = 1
    fl.close()
stopword(d)
#定义中文分词和停用词清洗,
# 注意：这里有一个bug，就是在用global的freq字典进行ajax向客服端传值的时候，会被重复赋值，而导致柱状图越来越密，其实可以单独做一个getWord函数，单独分词，但我觉得很影响效率，就算了
def cleancntxt(txt, stopwords):
    seg_generator = jieba.cut(txt,cut_all=True)
    seg_list = [i for i in seg_generator if i not in stopwords]
    global freq
    n = {}
    for word in seg_list:
        if word not in n:
            freq_n = seg_list.count(word)
            if freq_n > 20 and freq_n < 100:
                n[word] = freq_n
                freq["word"].append(word)
                freq["nums"].append(freq_n)
    return seg_list
# 定义中文词云函数
def wordcloudplot(txt):
    leaf = np.array(Image.open(path.join(d, "leaf.png")))
    wc = WordCloud(background_color="white", max_words=200, mask=leaf, font_path="msyh.ttc", max_font_size=150,
                   random_state=42)
    wc.generate(txt)

    wc.to_file(path.join("static", "wordcloud", "show1.png"))
# 文本清理函数
def TextClean(textpath):
    f = open(path.join(textpath, 'wordcloud_text.txt'), 'r', encoding='utf-8')
    text = ""
    for line in f.readlines():
        if re.match(r'^\d', line) == None:
            text = text + line
        else:
            pass
    f.close()
    return text

#总调用函数
def plotTitleCloud():
    txt = TextClean(d)
    seg_list = cleancntxt(txt, stopwords)
    txt = r' '.join(seg_list)
    wordcloudplot(txt)
