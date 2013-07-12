import MySQLdb
import json

print (cmd)
print (db)
print (query)

db = MySQLdb.connect(host="127.0.0.1", port=3306, db="mydb", user="root", passwd="ariag25")
cur = db.cursor()

cur.execute("SELECT * FROM users;")
return json.dumps (cur.fetchall())
