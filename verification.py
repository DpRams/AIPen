from flask import Flask, session
from flask_mail import Mail
from flask_mail import Message
from threading import Thread    
import sqlite3
import random




app = Flask(__name__)
app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PROT=465,
    MAIL_USE_TLS=True,
    MAIL_USERNAME='cbf1060208027@gmail.com',
    MAIL_PASSWORD='wfhsiao0208027'
)
#  記得先設置參數再做實作mail
mail = Mail(app)

def index(email):

    #  主旨
    msg_title = '驗證碼確認 '
    #  寄件者，若參數有設置就不需再另外設置
    msg_sender =('AIPEN', 'cbf1060208027@gmail.com')
    #  收件者，格式為list，否則報錯
    msg_recipients = [email]
    #  郵件內容
    # msg_body = 'Hey, I am mail body!'
    # 也可以利用html做內容

    with sqlite3.connect("SQLite\ARTICLE.db") as con:
             cursor = con.cursor()
             cursor.execute("SELECT vcode FROM Login where username='%s' " %(session.get("username")))
             result = cursor.fetchone()
             print(result[0])

    msg_html = result[0]
    msg = Message(msg_title,
                  sender=msg_sender,
                  recipients=msg_recipients)
    # msg.body = msg_body
    msg.html = msg_html

    #  使用多線程
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return 'You Send Mail by Flask-Mail Success!!'

def send_async_email(app, msg):
    #  下面有說明
    with app.app_context():
        mail.send(msg)




if __name__ == "__main__":
    app.debug = True
    
    app.run()