import sqlite3

db = sqlite3.connect('ARTICLE.db')
cursor = db.cursor()

# results = cursor.execute('''SELECT * FROM Kaochih ORDER BY RANDOM() LIMIT 1''')
# 學測 Kaochung 0809 13篇
# 統測 Kaochih 0809 6篇
# 660個題目 Titles
#SELECT column FROM table ORDER BY RAND() LIMIT 1
# SELECT * FROM Kaochih WHERE ID = 4

# for item in results:
#     arr = item
def get_posts():
    cursor.execute("SELECT * FROM Kaochung  where YEAR ='105' ")
    print(cursor.fetchall())

get_posts()

# arr = {}
# #x = len(arr)
# # print(x)    
# print(arr)
# print(arr[2])
# print(arr[3]) 
