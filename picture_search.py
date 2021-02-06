# -*- coding: utf-8 -*-
"""
Created on Wed Jul 15 00:22:53 2020

@author: User
"""

from pexels_api import API
from translate import Translator
#import googletrans 看起來很像是被Google ban掉了
from google_trans_new import google_translator
import jieba_zh_TW.jieba_.analyse 
import csv
import random

#2020/07/29

"""
備註:
此處為單純翻譯的套件，主要用googletrans(翻譯較好)，不過github文件表示其有可能會被限制，故準備另一個translator(翻譯較差)作備用
輸入:字串(中)
輸出:字串(英)
"""

def Chinese_to_English(word): 
    print("原本關鍵詞:"+word)
    translator = google_translator()  
    try:
        #translator = googletrans.Translator()
        word_trans = translator.translate(word,lang_tgt='en')
        print("Google套件的翻譯結果:"+word_trans)
        return word_trans

    except Exception as e:
        print(e)
        translator= Translator(from_lang="chinese",to_lang="english")
        word_trans = translator.translate(word)
        print ("translate套件的翻譯結果:"+word_trans)
        return word_trans
"""
備註:
try...except並沒有抓到API請求上限的錯誤，要再debug
如請求次數達到200次要替換API KEY
請在以下
 1.PEXELS_API_KEY = key_from_Tsai[0] 更改為 key_from_Ramsay[0]
 2.print(key_from_Tsai[1]) 更改為 key_from_Ramsay[1]
 以此類推
 
2020/07/30:目前丞哲的API KEY已經申請無限制存取

輸入:關鍵字(英文)
輸出:陣列(infos)
"""   
def Pexel_API(word_trans):
    photo_num = 0
    #key_from_Tsai = ('563492ad6f91700001000001480facdc0572451c8a0bcfd0eb371cdb',"Key from 旻均")
    key_from_Ramsay = ('563492ad6f91700001000001553202664e844eb2bab706a0a353889f',"Key from 丞哲")
    results_per_page = 1
    randnum = random.randint(0,6) #設定亂數讓他可以隨機生成 page從第幾頁開始
    try:
        info = []
        PEXELS_API_KEY = key_from_Ramsay[0]
        api = API(PEXELS_API_KEY)
        data = api.search(word_trans, results_per_page, randnum)

        photos = api.get_entries()
        
        print(key_from_Ramsay[1])
        # Loop the five photos
        for photo in photos:
            photo_num+=1

            print("\nImage "+str(photo_num))
            print('\nPhoto link(original size) : ', photo.original)
            
            info.append(photo.original)
            info.append(photo.id)
            info.append(photo.width)
            info.append(photo.height)
            info.append(photo.photographer)
            info.append(photo.description)
            info.append(photo.url)
                 
        if data['total_results'] == 0 or info == []:
            
            print("<-----------請往下個關鍵詞做搜尋----------->")
            
            return False,""
        else:
            print(info)
            print("------------------------------------------")
            return True, info #info[i][0]     
        
    except Exception as e:
        print(e)

rmv_char = ("!","！",",","，","、","；",";","。","()","（）")

"""
備註:移除不要的字元
"""
def Remove_char(text):
    #要直接填空的詞
    for x in rmv_char: 
        text = text.replace(str(x),"",1)
    #要取代成其他字元的詞
    return text

"""
備註:從文章中擷取關鍵字
輸入:文章(string)
輸出:文章關鍵字(list)
"""
def Extract(text):
    
    keywords = jieba_zh_TW.jieba_.analyse.tfidf(text, topK=10, withWeight=False, allowPOS=('n')) 
    while len(keywords) <= 10:
        keywords.append("快樂")
    return keywords

"""
備註:寫入圖片資料到csv，於網站上取出使用
"""
file = "Pexels_infos.csv"
def csv_write(infos):
    with open(file,"w",newline = "", encoding = 'utf-8') as f:
        fieldNames = ["Photo original size","id","width","height","photographer","description","url"]
    
        writer = csv.writer(f)
        writer.writerow(fieldNames)
        for i in infos:
            writer.writerow(i)
    
    
    
def main(sentence):
    keywords = Extract(sentence)
    links = []
    image_search = False
    while image_search == False:
        for i in range(0,len(keywords)):
            image_search, link = Pexel_API(Chinese_to_English(keywords[i]))
            if image_search == True:
                links.append(link)
            if len(links) == 4:
                break
        
    print("\nlinks:\n"+str(links))
    csv_write(links)

    print("\nPexels infos 已寫入{}".format(file))
    return links        
        

                
            
            

#------------------------------  



"""
main()回傳的links，給網站端拿去用作圖片超連結
main(文章句子,文章要分成幾段關鍵字去搜尋圖片(會有程式上限),一個關鍵字要搜尋幾張圖片)

2020/7/20 22:12
    1.目前已處理不滿四個圖片資料的問題，不過只算是權宜之計。並不是真正解決問題
    2.jieba取關鍵字目前讓不滿四段的文章，整段(輸出一維陣列)去找四個關鍵字而不是分四段(輸出二微陣列)找關鍵字
2020/07/30 19:47
    1.(已處理)有些關鍵字沒有那麼多頁的圖片可以用，造成其實並不是沒有資料而是沒有讀取到
    2.輸出的csvfile名稱改為Pexels_infos.csv
    
"""



            
            
            
            
            