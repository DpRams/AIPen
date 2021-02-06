# -*- coding: utf-8 -*-
"""
Created on Sat Jul  4 10:34:31 2020

@author: User
"""
"""
相關連結:
1.https://github.com/AguilarLagunasArturo/pexels-api
2.https://www.pexels.com/api/?locale=en-US

使用注意:
1.默認情況下，API的速率限制為每小時200個請求(不確定是200張還是200次請求)和每月20,000個請求。如果需要更高的限制，請與我們聯繫。
2.如果您符合我們的API條款，則可以免費獲得無限制的請求。
"""
"""
結論:多申請幾個API key的話，應該能在達限制之前，切換API key做交替使用
"""


# Import API class from pexels_api package
from pexels_api import API
from translate import Translator
import googletrans 

def Chinese_to_English():#套件出問題可用下一個套件
    print("原本字詞:"+word)
    try:
        translator= Translator(from_lang="chinese",to_lang="english")
        word_trans = translator.translate(word)
        print ("translate套件的翻譯結果:"+word_trans)
        return word_trans

    except Exception as e:
        print(e)
        translator = googletrans.Translator()
        word_trans = translator.translate(word)
        print("Google套件的翻譯結果:"+word_trans.text)
        return word_trans
        
def Pexel_API(word_trans, results_per_page, page):#金鑰達限制可用下一組金鑰
    photo_num = 0
    try:
        #旻均的金鑰
        PEXELS_API_KEY ='563492ad6f91700001000001480facdc0572451c8a0bcfd0eb371cdb'
        api = API(PEXELS_API_KEY)
        api.search(word_trans, results_per_page, page)
        # Get photo entries
        photos = api.get_entries()
        print("Key from 旻均")
        # Loop the five photos
        for photo in photos:
            photo_num+=1
            #print('Photographer: ', photo.photographer)
            #print('Photo url: ', photo.url)
            print("\nNo."+str(photo_num))
            print('\nPhoto original size: ', photo.original)
    except Exception as e:
        print(e)
        #丞哲的金鑰
        PEXELS_API_KEY ='563492ad6f91700001000001553202664e844eb2bab706a0a353889f'
        api = API(PEXELS_API_KEY)
        api.search(word_trans, results_per_page, page)
        # Get photo entries
        photos = api.get_entries()
        print("Key from 丞哲")
        # Loop the five photos
        for photo in photos:
            photo_num+=1
            #print('Photographer: ', photo.photographer)
            #print('Photo url: ', photo.url)
            print("\nNo."+str(photo_num))
            print('\nPhoto original size: ', photo.original)
"""
於以下輸入參數
Pexel_API(查詢字詞, 圖片數量, 頁碼)
查詢字詞:英文
圖片數量:1<=n<=80
頁碼:越低越好，越後面的頁數關聯性越低
"""  
  
word = input('input:')

Pexel_API(Chinese_to_English(), 4, 4)
        
print("\ndone")


