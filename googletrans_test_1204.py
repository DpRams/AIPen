from google_trans_new import google_translator  
  
translator = google_translator()  
translate_text = translator.translate('陪伴',lang_tgt='en')  
print(translate_text)
