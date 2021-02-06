#不要執行 除非有需要
import csv
import sqlite3

db = sqlite3.connect('ARTICLE.db')
cursor = db.cursor()
print("Connect Okay")

file = "統測歷屆作文.csv"

infos = []

with open(file, 'r', encoding='utf-8-sig' ) as csvfile: 
    rows = csv.reader(csvfile,delimiter = ',')

    for info in rows:
        print(info)

        cursor.execute('''INSERT INTO Kaochih (ID,YEAR,TITLE,DESCRIPTION,URL) VALUES(?,?,?,?,?)''',format(info[0],info[1],info[2],info[3],info[4]))
db.commit()