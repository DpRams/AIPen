# -*- coding: utf-8 -*-
"""
Created on Tue Aug 25 17:41:18 2020

@author: User
"""

import jieba_.analyse.tfidf
import jieba.analyse


text = "根據國際流星組織的資料，英仙座流星雨發生的時間從 7 月 13 日到 8 月 26 日，將近一個半月的時間，這段時間都可以看見英仙座流星雨。不過英仙座流星雨的極大期則是 8 月 13 日前後幾天，觀測條件好的地方，每小時最多可看見大約一百顆的英仙座流星！"



ans = jieba_.analyse.tfidf(text, topK=20, allowPOS = ('n'))
print("|".join(ans))
bns = jieba_.lcut(text)
print("|".join(bns))


def Extract(text):
    
    keywords = jieba.analyse.extract_tags(text, topK=10, withWeight=False, allowPOS=('n')) 
    while len(keywords) <= 4:
        keywords.append("快樂")
    return keywords

a = Extract(text)
print(a)