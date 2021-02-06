import smtplib
from email.mime.text import MIMEText
#https://myaccount.google.com/lesssecureapps 寄信帳號需先設定
#https://medium.com/jeasee%E9%9A%A8%E7%AD%86/python-email%E5%AF%84%E4%BF%A1-ba2b5eb05d6b
#https://support.google.com/a/answer/3726730?hl=zh-Hant

def mail(receiver, title, text):
    sender = ("CBF1060208027@gmail.com")
    html_1 = ("""
    <html>
        <head></head>
        <body>
            <p><h3>文章標題:<br></h3></p>
            %s
            <br>
            <p><h3>文章內容:<br></h3></p>
            %s
        </body>
    </html>
    """%(str(title),str(text)))

    
    message = MIMEText(html_1, "html", "utf-8")
    message["Subject"]="Story : {}".format(str(title))
    message["From"] = "AIPEN <CBF1060208027@gmail.com>"
    message["To"] = receiver
    message["Cc"] = None
    smtp = smtplib.SMTP("smtp.gmail.com", 587)
    smtp.ehlo()
    smtp.starttls()
    smtp.login(sender, "wfhsiao0208027") 
    smtp.sendmail(sender, receiver, str(message).encode('utf8'))

# mail("jason1120112011201120@gmail.com","生命","早安早安早安早安早安早安")