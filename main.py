from flask import Flask, render_template, request, redirect, url_for, session
import generate
import generate_practice
import picture_search
import torch
import torch.nn.functional as F
import os
import argparse
from tqdm import trange
from transformers import GPT2LMHeadModel
from datetime import timedelta
from pexels_api import API
from translate import Translator
import googletrans, random
from openpyxl import load_workbook
import csv
import pandas as pd
import sqlite3
import csv
from werkzeug.utils import secure_filename
import ocrspace
from flask import send_from_directory 
from flask import Flask
from flask_mail import Mail
from flask_mail import Message
from threading import Thread    
import verification
import forgive_password
import Mail



app = Flask(__name__)
app.config['SECRET_KEY'] = '123456'


# global ID

# @app.before_request
# def before_request():
#     db = sqlite3.connect('SQLite\ARTICLE.db')
#     cursor = db.cursor()
#     sql_count = "SELECT COUNT(*) FROM USER"
#     cursor.execute(sql_count)
#     _ = cursor.fetchone()
#     session["ID"] = _[0] + 1
    

@app.route("/",methods=['GET','POST'])
def index():
    regi=session.get('register')
    username=""
    username=session.get('username')
    if request.method == "POST":
       submit = request.form["job"]
       print(submit)
       if (submit=="validate"):
           return render_template('verification.html' ,username=username)
       if (submit=="logout"):
           session['username'] = "尚未登入"
           print(username)
           return render_template('index.html' ,username="尚未登入",register="" ) 

    #db = sqlite3.connect('SQLite\ARTICLE.db')
    #sql_drop = "DROP TABLE IF EXISTS USER"
    #sql_create = "CREATE TABLE IF NOT EXISTS USER(ID INT PRIMARY KEY NOT NULL, TITLE TEXT NOT NULL, TEXT TEXT NOT NULL)"

    #cursor.execute(sql_drop)
    #cursor.execute(sql_create)

    #db.commit()
    return render_template('index.html',username=username,register=regi)




@app.route("/get_properties",methods=['GET','POST'])
def get_properties():
    
    csv_file=csv.reader(open('Pexels_infos.csv','r',encoding='utf-8-sig'))
     #可以先輸出看一下該檔案是什麼樣的型別

    content=[] #用來儲存整個檔案的資料，存成一個列表，列表的每一個元素又是一個列表，表示的是檔案的某一行

    for line in csv_file:
        #列印檔案每一行的資訊
        content.append(line)
        print(content)
    #with open('images.csv','r',encoding='utf-8-sig')as f:
        #myCsvDic = csv.DictReader(f)
        #for row in myCsvDic:
           #a.append(row['id'])
           #print(row['id'])
   
    return render_template('get_properties.html',data=content)

@app.route("/model_generation", methods=['GET', 'POST'])
def model_generation():
    regi=session.get('register')
    username=session.get('username') 
    generate_or_save = ""
    value_1 = ""
    value_2 = ""
    value_3 = ""
    title =""
    subtitle =""
    mail = ""
    content = ""

    url1="" #先初始化
    url2=""
    url3=""
    url4=""
    links=[]
    i = random.randint(0,100) #設定亂數讓他可以隨機生成 page從第幾頁開始
    if request.method == "POST":
        
        generate_or_save = request.form["generate_or_save"]
        if generate_or_save == "generate":

            title = request.form["titles"]
            subtitle = request.form["subtitles"]
            value_1 = request.form["value_1"]
            value_3=int(value_1)
            generate.main(title,subtitle,value_3)
            print("here")
            with open(title+'.txt','r',encoding='utf-8-sig') as f:
                content=f.read()
                
            
            links=picture_search.main(content) #呼叫Pexel_API function
            print(links)      
            url1 = links[0][0]
            url2 = links[1][0]
            url3 = links[2][0]
            url4 = links[3][0]

            session["title"] = title
            session["text"] = content
        elif session.get("title") != "" and session.get("text") != "":

            try:
                
                db = sqlite3.connect('SQLite\ARTICLE.db')
                cursor = db.cursor()
                sql_count = "SELECT COUNT(*) FROM USER"
                sql_max = "SELECT MAX(ID) FROM USER"
                cursor.execute(sql_count)
                count = cursor.fetchone() #資料筆數
                if (count[0]) < 1 :
                    session["ID"] =  1

                else:
                    cursor.execute(sql_max)
                    max_ = cursor.fetchone()
                    session["ID"] = max_[0] + 1
                cursor.execute("INSERT INTO USER (username,ID, TITLE, TEXT) VALUES (?,?,?,?)",(username,session["ID"], session["title"],session["text"]))
                db.commit()
                session["title"] =""
                session["text"] = ""


            except Exception as e:
                print(e)
        #content = content.replace("鞦天","秋天")
        return render_template("model_generation.html",content=content,data1 = url1,data2 = url2,data3 = url3,data4= url4,title=title,username=username,register=regi)
    if request.method == "POST":
        logoutbtn = request.form["logoutbtn"]
        print( logoutbtn)
        if (logoutbtn==""):
            session['username'] = "尚未登入"
            return render_template('index.html',username=username)
       
        
        
        
    return render_template("model_generation.html",data1= url1,data2= url2,data3= url3,data4= url4,username=username,register=regi) #最先導入的頁面
@app.route("/login", methods=["POST","GET"])
def login():          

    if request.method == "POST":
        username = request.form["usr"]
        password = request.form["pwd"]
        print(username, password)
        with sqlite3.connect("SQLite\ARTICLE.db") as con:
             cursor = con.cursor()
             cursor.execute("SELECT * FROM Login where username='%s'AND password ='%s' " %(username, password ))
             result = cursor.fetchone()
             print(result)
             if (result!=None):
                  session['username'] = username
                  print( session['username'])
                  cursor.execute("SELECT email FROM Login where username='%s'AND password ='%s' " %(username, password ))
                  email = cursor.fetchone()
                  session['mail']= email[0] #此處格式不為字串
                  cursor.execute("SELECT register FROM Login where username='%s'AND password ='%s' " %(username, password ))
                  regi=cursor.fetchone()
                  session['register']=regi[0]
                  return render_template('index.html',username=username,register=regi[0])
                
             else:                
                  return render_template('login.html',error="error")
            
        
    return render_template("login.html")

@app.route('/register', methods=['GET', 'POST'])
def register():
     
    
     if request.method == 'POST':
             
         username = request.form["usr"]
         password = request.form["pwd"]
         email = request.form["email"]
         birth=request.form["birth"]
         phone=request.form["phone"]
         print(username, password, email)
         with sqlite3.connect("SQLite\ARTICLE.db") as con:
              cursor = con.cursor()
              cursor.execute("SELECT * FROM Login where username='%s'" %(username))   
              result = cursor.fetchone()
              cursor.execute("SELECT * FROM Login where email='%s' " %(email))  
              resultmail = cursor.fetchone()
              print(result)
              if (result!=None):
                  return render_template('register.html',repeat="repeat") 
              elif(resultmail!=None):
                  return render_template('register.html',mailrepeat="mailrepeat")
              else:                 
                  captcha = str( random.randint(0,999999))
                  captcha  = captcha .zfill(6)
                  cursor.execute("INSERT INTO Login (username, password, email,birth,phone,vcode) VALUES (?,?,?,?,?,?)", (username, password, email,birth,phone,captcha))
                  session['username'] = username
                  session['vcode'] = captcha
                  session['email'] = email
                  con.commit()
                  print("註冊成功")
                  verification.index(email)
                  return redirect(url_for('validate'))
              con.close()
         

     return render_template('register.html')
 
@app.route('/verification', methods=["POST","GET"])
def validate():          

    if request.method == "POST":
        submit=request.form["job1"]
        vnum = request.form["vnum"]
        username=session.get('username')
        if(submit=="validate"):

            with sqlite3.connect("SQLite\ARTICLE.db") as con:
                cursor = con.cursor()
                cursor.execute("SELECT * FROM Login where vcode='%s' AND username='%s' " %(vnum,username))
                result = cursor.fetchone()
                print(result)
                if (result!=None):
                    #session['vcode'] = vnum
                    cursor.execute("UPDATE Login SET register=1 WHERE username='%s'; " %(username))
                    cursor.execute("SELECT register FROM Login where username='%s' " %(username))
                    regi=cursor.fetchone()
                    con.commit()
                    return render_template('index.html',username=username,register=regi[0])
                else:                
                    return render_template('verification.html',error="error")
                con.close()
        elif(submit=="send"):
            email=[""]
            with sqlite3.connect("SQLite\ARTICLE.db") as con:
                cursor = con.cursor()
                cursor.execute("SELECT email FROM Login where username='%s' " %(session.get("username")))
                email = cursor.fetchone()

            print(email[0])
            
            verification.index(email[0])
    
    return render_template("verification.html")

@app.route("/forgive",methods=['GET','POST'])
def forgive():
    mail=""
    email=""
    db = sqlite3.connect('SQLite\ARTICLE.db')
    cursor = db.cursor()
    if request.method == "POST":
         mail = request.form["email"]
         print(mail)
         session['remail']=mail
         cursor.execute("SELECT * FROM Login where email='%s' " %(mail))
         email = cursor.fetchone()
         db.close()
         print(email)
         if email==None:
            return render_template("forgive.html",alert=0)
         else:
             captcha = str( random.randint(0,999999))
             captcha  = captcha .zfill(6)
             print(captcha)
             forgive_password.index(mail,captcha)
             return render_template("forgive.html",mail=mail,alert=1,code=captcha)
    return render_template("forgive.html",alert=2)


@app.route("/password_reset",methods=['GET','POST'])
def password_reset():
     password=""
     username=session['username'] = "尚未登入"
     print( session['username'])
     if request.method == "POST":
          password = request.form["pwd"]
          mail=session['remail']
          print(mail)
          db = sqlite3.connect('SQLite\ARTICLE.db')
          cursor = db.cursor()
          cursor.execute("UPDATE Login SET password='%s' WHERE email='%s'; " %(password,mail))
          db.commit()
          db.close()
          session['remail']=""
          return render_template("login.html",username="尚未登入")
     return render_template("password_reset.html",username="尚未登入")

@app.route("/topic_generation", methods=["POST","GET"]) #題目生成
def topic_generation():
   
    username=session.get('username')
    regi=session.get('register')
    url = ""
    bool_1 = ""
    bool_2 = ""

    value_1 = "" #學測or統測選項
    value_2 = "" #年度選項
    value_3 = ""
    ID = 0
    times = 0
    titles = []
    outputs = []    

    templates = ""
    topic = "" #生成範文題目欄位
    description = "" #生成范文說明欄位
    action = "" #0813未用到

    db = sqlite3.connect('SQLite\ARTICLE.db')
    cursor = db.cursor()
    if request.method == "POST":
        regi=session.get('register')
        bool_1 = request.form["bool_1"]
        bool_2 = request.form["bool_2"]
        if bool_1 == "true" and bool_2 == "false":
            value_3 = request.form["value_3"]
            results = cursor.execute(f"SELECT * FROM Titles ")
            for item in results:
                titles.append(item[1])
            random.shuffle(titles)
            
            for i in range(0,int(value_3)):
                print(titles[i])
                outputs.append(titles[i])
            
        else:
            value_1 = request.form["value_1"]
            if value_1 != "0":
                value_2 = request.form["value_2"]
                sql = "SELECT * FROM {} where Year = '{}' ORDER BY RANDOM() LIMIT 1".format( value_1,value_2 ) 
                db = sqlite3.connect('SQLite\ARTICLE.db')
                cursor = db.cursor()
                results = cursor.execute(sql)  #SELECT * FROM(選擇的高中或高職) WHERE 年度(選擇的年度) ORDER BY 隨機選取
                print(results)
                for item in results:
                    description += str(item[3])  #將說明輸出
                    topic += str(item[2]) #將題目輸出
                    print(topic)
        return render_template("topic_generation.html" ,data = url, outputs = outputs , topic = topic, formdata3 = description,username=username,register=regi)
        logoutbtn = request.form["logoutbtn"]
        print( logoutbtn)
        if (logoutbtn==""):
            session['username'] = "尚未登入"
            return render_template('index.html',username=username)     
            
    return render_template("topic_generation.html" ,data = url, outputs = outputs , topic = topic, formdata3 = description,username=username,register=regi )
    
    # # return render_template("topic_generation.html" ,data = url, formdata = "3", formdata2 = topic + "2", formdata3 = value_1+"1,"+ description)
    # return render_template("topic_generation.html")



@app.route("/article_practice", methods=['GET', 'POST'])
def article_practice():
    regi=session.get('register')
    username=session.get('username')
    print(username)
    subtitle=""
    user_title=""
    lbl = ""
    tip = ""
    user_text = ""
    user_text_split = ""
    formdata = ""
    number=0
    number2=0
    
    
    with open ( '句子.csv','r',encoding='utf-8-sig' ) as in_file:  
        with open ( '文章候選句子.csv' , 'w' , newline= '', encoding='utf-8-sig') as out_file:  
            writer = csv. writer ( out_file )
            for row in csv. reader ( in_file ) :
                if any ( field. strip () for field in row ) :  
                    writer. writerow ( row )
    csv_file=csv.reader(open('文章候選句子.csv','r',encoding='utf-8-sig'))
    content=[]
    random_number=[]
    for line in csv_file:        
        content.append(line)
        number+=1
    for i in range(number):
        random_number.append(i)
    random.shuffle(random_number) 
    print(number)
    print(random_number)
    data1=content[random_number[0]][0]
    data2=content[random_number[1]][0]
    data3=content[random_number[2]][0]
    data4=content[random_number[3]][0]
    data5=content[random_number[4]][0]
    if request.method == "POST":
        number=0
        content_length=0
        user_title = request.form["user_title"]#0821                
        user_text = request.form['user_text']
        content_length=len(user_text)       
        lbl = request.form["lbl"]
        btn = request.form["btn"]
        #if (len( user_text)>=50):
            #user_text_split=user_text
            #user_text_split=user_text_split.replace(",","，")
            #print(user_text_split)
            #user_text_split=user_text_split.split("，")           
            #print(user_text_split)
            #user_text_split=user_text_split[-3]+"，"+user_text_split[-2]+"，"+user_text_split[-1]
            #print(user_text_split)
        if btn == "btip_1":
            tip = lbl
            generate_practice.main(user_title,(user_text + tip),content_length) 
        elif btn == "btip_2":
            tip = lbl
            generate_practice.main(user_title,(user_text + tip),content_length) 
        elif btn == "btip_3":
            tip = lbl
            generate_practice.main(user_title,(user_text + tip),content_length) 
        elif btn == "btip_4":
            tip = lbl
            generate_practice.main(user_title,(user_text + tip),content_length) 
        elif btn == "btip_5":
            tip = lbl
            generate_practice.main(user_title,(user_text + tip),content_length) 
        elif btn =="btip_6":
            generate_practice.main(user_title,user_text ,content_length)
        elif btn =="b_save" and user_title != "" and user_text != "":

            formdata = user_text + tip 

            db = sqlite3.connect('SQLite\ARTICLE.db')
            cursor = db.cursor()
            sql_count = "SELECT COUNT(*) FROM USER"
            sql_max = "SELECT MAX(ID) FROM USER"
            cursor.execute(sql_count)
            count = cursor.fetchone() #資料筆數
            if (count[0]) < 1 :
                session["ID"] =  1

            else:
                
                cursor.execute(sql_max)
                max_ = cursor.fetchone()
                session["ID"] = max_[0] + 1
            cursor.execute("INSERT INTO USER (username,ID, TITLE, TEXT) VALUES (?,?,?,?)",(username,session["ID"], user_title, formdata))
            db.commit()

        formdata = user_text + tip 
        with open ( '句子.csv','r',encoding='utf-8-sig' ) as in_file:  
            with open ( '文章候選句子.csv' , 'w' , newline= '', encoding='utf-8-sig') as out_file:  
                writer = csv. writer ( out_file )
                for row in csv. reader ( in_file ) :
                    if any ( field. strip () for field in row ) :  
                        writer. writerow ( row )

        csv_file=csv.reader(open('文章候選句子.csv','r',encoding='utf-8-sig'))
        content=[]        
        for line in csv_file:        
            content.append(line)
            number2+=1
        print(number2)
        data1=content[number2-5][0]
        data2=content[number2-4][0]
        data3=content[number2-3][0]
        data4=content[number2-2][0]
        data5=content[number2-1][0]
        print(data1)
        print(data2)
        print(data3)
        print(data4)
        print(data5)   
        
                                                        #0821
        return render_template("article_practice.html",username=username,title = user_title,formdata = formdata,data1=data1,data2=data2,data3=data3,data4=data4,data5=data5,register=regi)  
        logoutbtn = request.form["logoutbtn"]
        print( logoutbtn)
        if (logoutbtn==""):
           session['username'] = "尚未登入"
           return render_template('index.html',username=username)   
    return render_template("article_practice.html",username=username,title = user_title,formdata = formdata,data1=data1,data2=data2,data3=data3,data4=data4,data5=data5,register=regi)  

UPLOADED_FOLDER = os.path.join(os.getcwd(), 'static\\upload')                        
ALLOWED_EXTENSIONS = set(['pdf', 'png', 'jpg', 'jpeg', 'gif'])

app.config['UPLOADED_FOLDER'] = UPLOADED_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS
           
@app.route("/article_scan", methods=['GET','POST']) #作文掃描
def article_scan():
    regi=session.get('register')
    username=session.get('username')
    print( username)
    if request.method == 'POST':    
        file = request.files['file']      
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOADED_FOLDER'],filename)) 
            fileurl="../static/upload/"+filename
            print(fileurl)            
            content=usingapi(filename)
            return render_template("article_scan.html",content=content,fileurl=fileurl,username=username)  
        logoutbtn = request.form["logoutbtn"]
        print( logoutbtn)
        if (logoutbtn==""):
            session['username'] = "尚未登入"
            return render_template('index.html',username=username)
      
    return  render_template("article_scan.html",username=username,register=regi)  

@app.route("/mail_to_user", methods=['GET','POST']) #寄發作文
def mail_to_user():
    vadi=[""]
    username=session.get('username')
    with sqlite3.connect("SQLite\ARTICLE.db") as con:
        cursor = con.cursor()
        cursor.execute("SELECT register FROM Login where username='%s' " %(username))
        vadi=cursor.fetchone()
        if vadi == None:
            vadi = [""]
        print(vadi[0])
    if (username== "尚未登入" or username== None):  
        return render_template("mail_to_user.html",warning="請登入")
    elif(vadi[0] == 0 ):
        return render_template("mail_to_user.html",warning="請驗證")
    # db = sqlite3.connect('SQLite\ARTICLE.db')
    # cursor = db.cursor()
    # sql_select = "SELECT * FROM USER"
    # results = cursor.execute(sql_select)
    article = []
    articles = []
    # index = 1
    # for item in results:
    #     article.append(item[0])
    #     article.append(item[1])
    #     article.append(item[2])
    #     articles.append(article)
    #     article = []
    #     index += 1

    if request.method == "POST":
        address = ""
        title = ""
        text = ""
     
        mail_id = 0
        rmv_id = 0

        mail_rvs_rmv = request.form["mail_rvs_rmv"]



        if mail_rvs_rmv == "rmv":
            rmv_id = request.form["rmv"]
            db = sqlite3.connect('SQLite\ARTICLE.db')
            cursor = db.cursor()
            sql_delete = "DELETE FROM USER WHERE ID = '{}'".format(rmv_id)
            cursor.execute(sql_delete)
            db.commit()
            

        elif mail_rvs_rmv == "mail":
            mail_id=request.form["email"]
            address = session.get('mail')
            title = request.form["title_input"]
            text = request.form["text_input"]
            print(text)
            Mail.mail(address, title, text)

        elif mail_rvs_rmv == "rvs":
            rvs_id = request.form["rvs"]

            title = request.form["title_input"]
            text = request.form["text_input"]

            db = sqlite3.connect('SQLite\ARTICLE.db')
            cursor = db.cursor()
            
            sql_revise = "UPDATE USER SET TITLE = '{0}', TEXT = '{1}' WHERE ID = '{2}'".format(title, text, rvs_id)
            cursor.execute(sql_revise)
            db.commit()
   


    db = sqlite3.connect('SQLite\ARTICLE.db')
    cursor = db.cursor()
    sql_select = "SELECT * FROM USER where username ='{}'".format(username)
    results = cursor.execute(sql_select)
    article = []
    articles = []

    for item in results:
        article.append(item[1])
        article.append(item[2])
        article.append(item[3])
        articles.append(article)
        article = []
    regi=session.get('register')
    return  render_template("mail_to_user.html", articles = articles,username=username,register=regi) 
    
    if request.method == "POST":
        logoutbtn = request.form["logoutbtn"]
        print( logoutbtn)
        if (logoutbtn==""):
            session['username'] = "尚未登入"
            return render_template('index.html',username=username)    

    
def usingapi(filename):
    api = ocrspace.API('e8f4e1d2ab88957', ocrspace.Language.Chinese_Traditional)
    print(UPLOADED_FOLDER)
    content=format(api.ocr_file(open('{0}/{1}'.format(UPLOADED_FOLDER,filename), 'rb')))
    return content



if __name__ == "__main__":
    app.run(debug=True)
