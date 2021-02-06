import sqlite3

db = sqlite3.connect('ARTICLE.db')
cursor = db.cursor()

results = cursor.execute('''SELECT * FROM Kaochih WHERE ID = 7''')
for item in results:
    print(item)