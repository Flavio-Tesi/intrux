import MySQLdb

db = MySQLdb.connect(host="127.0.0.1", port=3306, db="mydb", user="root", passwd="ariag25")
cur = db.cursor()

def read_users():
	cur.execute("SELECT * FROM users;")
	return cur.fetchall()
		
def read_userCode (i):
	cur.execute("SELECT code FROM users WHERE id=%d;" %i)
	return cur.fetchone()[0]
		
def read_userName (i):
	cur.execute("SELECT name FROM users WHERE id=%d;" %i)
	return cur.fetchone()[0]

def set_userCode (i, code):
	cur.execute("UPDATE users SET code=%d WHERE id=%d;" %(code,i))
	db.commit()
	
def read_temperatures():
	cur.execute ("SELECT * FROM temperatures;")
	return cur.fetchall()
		
def read_temperature(i):
	cur.execute ("SELECT val FROM temperatures WHERE room=%s;" %i)
	return cur.fetchone()[0]
		
def set_temperature(i, val):
	cur.execute ("UPDATE temperatures SET val=%d WHERE room=%d;" %(val,i))
	db.commit()
	
def read_lights():
	cur.execute ("SELECT * FROM lights;")
	return cur.fetchall()

def read_light(i):
	cur.execute ("SELECT status FROM lights WHERE id=%d;" %i)
	return cur.fetchone()[0]
	
def change_light(i):
	x = read_light(i)
	if x == 0:
		x = 1
	elif x == 1:
		x = 0
	cur.execute ("UPDATE lights SET status=%d WHERE id=%d;" %(x,i))
	db.commit()
	
def read_intrusions():
	cur.execute ("SELECT * FROM intrusions;")
	return cur.fetchall()

def read_intrusion(i):
	cur.execute ("SELECT status FROM intrusions WHERE id=%d;" %i)
	return cur.fetchone()[0]
	
def change_intrusion(i):
	x = read_intrusion(i)
	if x == 0:
		x = 1
	elif x == 1:
		x = 0
	cur.execute ("UPDATE intrusions SET status=%d WHERE id=%d;" %(x,i))
	db.commit()
