import MySQLdb
import time

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
	
def read_rooms():
	cur.execute("SELECT * FROM rooms;")
	return cur.fetchall()
	
def read_room(i):
	cur.execute("SELECT name FROM rooms WHERE id=%d;" %i)
	return cur.fetchone()[0]
	
def add_room(name):
	cur.execute ("INSERT INTO rooms (name) VALUES, (%s);" %name)
	db.commit()
	
def read_lights():
	cur.execute ("SELECT * FROM lights, rooms WHERE lights.id_room = room.id;")
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
	
def read_temperatures():
	cur.execute ("SELECT * FROM temperatures, rooms WHERE temperatures.id_room = rooms.id ORDER BY dat;")
	return cur.fetchall()
		
def read_temperature(i):
	cur.execute ("SELECT val FROM temperatures WHERE id=%d;" %i)
	return cur.fetchone()[0]
	
def read_logTempRoom(id_room):
	cur.execute("SELECT * FROM temperatures WHERE id_room=%d;" %id_room)
	return cur.fetchall()

def read_logTempData(dat):
	cur.execute("SELECT * FROM temperatures WHERE dat=%Y-%m-%d;" %dat)
	return cur.fetchall()
	
def read_logTempRD(id_room, dat):
	cur.execute("SELECT * FROM temperatures WHERE dat=%Y%m%d && id_room=%d;" %(dat, id_room))
	return cur.fetchall()
	
def set_temperature(id_room, val, dat, ora):
	cur.execute ("INSERT INTO temperatures (id_room, val, dat, dattime) VALUES, (%d, %d, %Y%m%d, %H:%M:%S);" %(id_room, val, dat, ora))
	db.commit()

def read_intrusions():
	cur.execute ("SELECT * FROM intrusions;")
	return cur.fetchall()

def read_intrusion(i):
	cur.execute ("SELECT status FROM intrusions WHERE id=%d;" %i)
	return cur.fetchone()[0]

def read_logIntrRoom(id_room):
	cur.execute("SELECT * FROM intrusions WHERE id_room=%d;" %id_room)
	return cur.fetchall()

def read_logIntrData(dat):
	cur.execute("SELECT * FROM intrusions WHERE dat=%Y-%m-%d;" %dat)
	return cur.fetchall()
	
def read_logIntrRD(id_room, dat):
	cur.execute("SELECT * FROM intrusions WHERE dat=%Y%m%d && id_room=%d;" %(dat, id_room))
	return cur.fetchall()
	
def set_intrusion(id_room, status, dat, dattime):
	cur.execute ("INSERT INTO intrusions (id_room, status, dat, dattime) VALUES, (%d, %d, %Y%m%d, %Y%m%d %H:%M:%S);" %(id_room, status, dat, dattime))
	db.commit()
