import pymongo
import jieba
from wordcloud import WordCloud
from spoon.spoon.settings import *


top_n = 100

client = pymongo.MongoClient(MONGO_URI)
db = client[MONGO_DATABASE]

counter = dict()
items = list(db["top_summary"].find())
for item in items:
    summary = item['summary']
    summary_list = [word for word in list(jieba.cut(summary, cut_all=False)) if len(word) >= 2]
    # word_list.extend(summary_list)
    print(summary, "[", "/ ".join(summary_list), "]")

    for word in summary_list:
        if word in counter.keys():
            counter[word] += 1
        else:
            counter[word] = 1

sorted_list = sorted(counter.items(), key=lambda item : item[1], reverse=True)
top_n_word = [word[0] for word in sorted_list]
if top_n > 0:
    top_n_word = top_n_word[:top_n]

w = WordCloud(width=1920, height=1080, font_path='/usr/share/fonts/truetype/arphic/ukai.ttc')
w.generate(" ".join(top_n_word))
w.to_file("summary.png")