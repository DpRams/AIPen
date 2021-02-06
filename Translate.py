# -*- coding: utf-8 -*-
"""
Created on Sat Jul  4 11:06:33 2020

@author: User
"""
#------------------------------------------------
"""
相關連結:
1.googletrans連結
https://github.com/ssut/py-googletrans    
    
2.[Python] 使用 googletrans 套件來進行 Google 翻譯
https://clay-atlas.com/blog/2020/05/05/python-cn-note-package-googletrans-google-translate/

3.送你一個免費的python萬國語言翻譯器
https://kknews.cc/zh-tw/code/n6lqmo3.html

使用注意:
1.字串長度不得超過 15000 個字元
2.這是使用 web API of translate.google.com 且與Google企業無關聯 
3.網頁更新時，需等此套件更新才能正常運作。所以如果要非常穩定的使用這項功能，建議直接用Google官方的翻譯API。定價連結https://cloud.google.com/translate/pricing
4.HTTP 5xx Error 即代表 Google 封鎖了 IP 位址
"""
#------------------------------------------------
"""
相關連結:
1.translate連結
https://github.com/terryyin/translate-python

2.https://pypi.org/project/translate/

使用注意:
1.無任何限制
2.相較於googletrans，我覺得此款套件更於穩定，且同樣足夠維持使用
"""
#------------------------------------------------
"""
結論:兩套應可搭著一起用，寫try catch，一個出問題就搭另外一個
"""

from translate import Translator
import googletrans 
#from pprint import pprint
#------------------------------------------------

word = '屁股'
print("原本句子:"+word)
translator= Translator(from_lang="chinese",to_lang="english")
word_trans = translator.translate(word)
print ("translate套件的翻譯結果:"+word_trans)

#------------------------------------------------

# Initial
translator = googletrans.Translator()


# Basic Translate
results = translator.translate(word)
#print(results)
print("Google套件的翻譯結果:"+results.text)