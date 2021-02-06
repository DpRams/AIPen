#不要執行 除非有需要
import sqlite3

db = sqlite3.connect('ARTICLE.db')
cursor = db.cursor()
print("Connect Okay")
#Kaochih Kaochung Titles
# cursor.execute(
# """CREATE TABLE Kaochih
# (ID INT PRIMARY KEY NOT NULL,
# YEAR INT NOT NULL,
# TITLE TEXT NOT NULL,
# DESCRIPTION TEXT,
# URL TEXT);""")

#cursor.execute("CREATE TABLE Login (username VARCHAR PRIMARY KEY  UNIQUE NOT NULL, password VARCHAR NOT NULL, email VARCHAR NOT NULL  UNIQUE, birth  DATE NOT NULL, phone VARCHAR NOT NULL);")
cursor.execute("select * from Login")
result_set = cursor.fetchall()
print(result_set)

db.commit()



# cursor.execute(
#     '''INSERT INTO Kaochung (ID,YEAR,TITLE,DESCRIPTION,URL) VALUES (1, 106,'關於經驗的N種思考','', 25)''')