import tornado.httpserver
import tornado.ioloop
import tornado.web
import json
import db_query
import datetime
import threading
import daisy_function
import time
import comandi_shell
import rfid
import send_email

"""
import screen_read
class ThreadScreen(threading.Thread):													#thread per schermo
	def run(self):
		while True:
			screen_read.function()
			time.sleep(0.5)	
ts = ThreadScreen()
ts.daemon = True
ts.start()

class ThreadTemp(threading.Thread):														#thread per log temperature
	def run(self):
		while True:
			time.sleep(1800)
tt = ThreadTemp()
tt.daemon = True
tt.start()

"""

class ThreadCompactPics(threading.Thread):												#thread per video cam
	def run(self):
		while True:
			comandi_shell.compact_image()
			time.sleep(3600)	
tl = ThreadLuci()
tl.daemon = True
tl.start()

class ThreadRecordCam(threading.Thread):												#thread per record cam
	def __init__(self):
		super(ThreadRecordCam, self).__init__()
		self._stop = threading.Event()
	def stop(self):
		self._stop.set()
	def run(self):
		comandi_shell.on_record()
trc = ThreadRecordCam()
trc.daemon = True

class ThreadCam(threading.Thread):														#thread per cam
	def __init__(self):
		super(ThreadCam, self).__init__()
		self._stop = threading.Event()
	def stop(self):
		self._stop.set()
	def run(self):
		comandi_shell.on_cam_640_480()	
tc = ThreadCam()
tc.daemon = True

class ThreadCamHD(threading.Thread):													#thread per cam
	def __init__(self):
		super(ThreadCamHD, self).__init__()
		self._stop = threading.Event()
	def stop(self):
		self._stop.set()
	def run(self):
		comandi_shell.on_cam_1280_720()
tchd = ThreadCamHD()
tchd.daemon = True

class ThreadAllarme(threading.Thread):													# thread allarme
	def __init__(self):
		super(ThreadAllarme, self).__init__()
		self._stop = threading.Event()
	def stop(self):
		self._stop.set()
	def stopped(self):
		return self._stop.isSet()					
	def run(self):
		while not(self.stopped()):
			daisy_function.allarme()
			time.sleep(0.1)					
ta = ThreadAllarme()
ta.daemon = True
ta.stop()

class ThreadLuci(threading.Thread):														#thread per luci
	def run(self):
		while True:
			daisy_function.luci()
			time.sleep(0.1)	
tl = ThreadLuci()
tl.daemon = True
tl.start()

class ThreadRFID(threading.Thread):														#thread per rfid
	def run(self):
		while True:
			if rfid.function() == "admin": 
				if ta.stopped():
					ta.__init__()
					ta.start()
				else:
					daisy_function.stop_allarme()
					ta.stop()
			if (rfid.function() == "user"):
				if ta.stopped():
					ta.__init__()
					ta.start()
				else:
					daisy_function.stop_allarme()
					ta.stop()
					send_email.invia_email_rfid_utente()
				
			time.sleep(0.1)	
tr = ThreadRFID()
tr.daemon = True
tr.start()

class execute(tornado.web.RequestHandler):
	def get(self):
		if self.get_argument('cmd')=="read_users":										#lettura utenti
			self.write(json.dumps(db_query.read_users()))
		elif self.get_argument('cmd')=="read_lights":									#lettura luci
			self.write(json.dumps(db_query.read_lights()))
		elif self.get_argument('cmd')=="change_light":									#modifica luci
			i = int(self.get_argument('id'))
			daisy_function.funzioni[i-1]()
		elif self.get_argument('cmd')=="set_usercode":									#imposta password
			i = int(self.get_argument('id'))
			if self.get_argument('pwd0')=='a':
				self.write("INSERIRE UNA PASSWORD VALIDA")
			elif int(self.get_argument('pwd0'))==int(db_query.read_userCode(i)):
				new_pwd = self.get_argument('pwd1')
				if new_pwd == self.get_argument('pwd2'):
					db_query.set_userCode(i, int(new_pwd))
					self.write("PASSWORD CORRETTAMENTE MODIFICATA")
				else:
					self.write("PASSWORD NON CORRISPONDENTI")
			else:
				self.write("PASSWORD ERRATA")	
		elif self.get_argument('cmd')=="verify_user":									#verifica per login
			username = str(self.get_argument('id'))
			password = str(self.get_argument('pwd'))
			usr = db_query.read_users()
			if (usr[0][1] == username) & (usr[0][2] == password):
				self.write ("LOGIN ADMIN")
			elif (usr[1][1] == username) & (usr[1][2] == password):
				self.write ("LOGIN USER")
			else:
				self.write ("LOGIN FAIL")
		elif self.get_argument('cmd')=="read_intrusions":								#lettura intrusioni
			self.write(json.dumps(db_query.read_intrusions()))
		
		elif self.get_argument('cmd')=="stop_allarme":									#ferma allarme	
			daisy_function.stop_allarme()
			ta.stop()
		elif self.get_argument('cmd')=="start_allarme":									#avvia allarme	
			if ta.stopped():
				ta.__init__()
				ta.start()
		elif self.get_argument('cmd')=="on_cam":										#accendi cam a bassa risoluzione
			comandi_shell.off_cam()
			time.sleep(1)
			tc.__init__()
			tc.start()	
			time.sleep(2)
		elif self.get_argument('cmd')=="on_cam_hd":										#accendi cam a alta risoluzione
			comandi_shell.off_cam()
			time.sleep(1)
			tchd.__init__()
			tchd.start()
			time.sleep(2)
		elif self.get_argument('cmd')=="off_cam":										#spegni cam
			tc.stop()
			tchd.stop()
			comandi_shell.off_cam()	
		elif self.get_argument('cmd')=="record_video":									#record cam
			tc.stop()
			tchd.stop()
			comandi_shell.off_cam()	
			trc.__init__()
			trc.start()
		elif self.get_argument('cmd')=="stop_record_video":								#stop record cam
			trc.stop()
			comandi_shell.off_record()	
			comandi_shell.convert_video(x)
		
		
		elif self.get_argument('cmd')=="temp_room":										#lettura temperature
			rm = str(self.get_argument('rm'))
			di = str(self.get_argument('di'))
			df = str(self.get_argument('df'))
			if (rm == "xx") & (di == "xx") & (df == "xx"):
				x = db_query.read_temperatures()
				y = []
				for i in x:
					a = (i[0], i[1], i[2], str(i[3]), str(i[4]))
					y.append(a)
				self.write(json.dumps(y))
			elif (rm == "xx") & (di == "xx") & (df != "xx"):
				self.write("INSERIRE UNA DATA DI INIZIO")
			elif (rm == "xx") & (di != "xx") & (df == "xx"):
				self.write("INSERIRE UNA DATA DI FINE")
			elif (rm == "xx") & (di != "xx") & (df != "xx"):
				di = datetime.datetime.strptime(str(self.get_argument('di')), "%m/%d/%Y")
				df = datetime.datetime.strptime(str(self.get_argument('df')), "%m/%d/%Y")
				if di>df:
					dttemp = di
					di = df
					df = dttemp
				x = []
				while (di<=df):
					y=db_query.read_logTempData(datetime.datetime.strftime(di,"%Y-%m-%d"))
					if (y != ()):
						for k in y:
							x.append(k)
					di = di + datetime.timedelta(days=1)
				j=[]
				for i in x:
					a = (i[0], i[1], i[2], str(i[3]), str(i[4]))
					j.append(a)
				self.write(json.dumps(j))
			elif (rm != "xx") & (di == "xx") & (df == "xx"):
				rm = int(str(self.get_argument('rm'))[0])
				x = db_query.read_logTempRoom(rm)
				y = []
				for i in x:
					a = (i[0], i[1], i[2], str(i[3]), str(i[4]))
					y.append(a)
				self.write(json.dumps(y))
			elif (rm != "xx") & (di == "xx") & (df != "xx"):
				self.write("INSERIRE UNA DATA DI INIZIO")
			elif (rm != "xx") & (di != "xx") & (df == "xx"):
				self.write("INSERIRE UNA DATA DI FINE")
			else:
				rm = int(str(self.get_argument('rm'))[0])
				di = datetime.datetime.strptime(str(self.get_argument('di')), "%m/%d/%Y")
				df = datetime.datetime.strptime(str(self.get_argument('df')), "%m/%d/%Y")
				if di>df:
					dttemp = di
					di = df
					df = dttemp
				x = []
				while (di<=df):
					y=db_query.read_logTempRD(rm, datetime.datetime.strftime(di,"%Y-%m-%d"))
					if (y != ()):
						for k in y:
							x.append(k)
					di = di + datetime.timedelta(days=1)
				j=[]
				for i in x:
					a = (i[0], i[1], i[2], str(i[3]), str(i[4]))
					j.append(a)
				self.write(json.dumps(j))
		elif self.get_argument('cmd')=="read_rooms":									#lettura stanze
			self.write(json.dumps(db_query.read_rooms()))		
		
		
		
application = tornado.web.Application([
	(r"/execute", execute),
	(r"/(.*)", tornado.web.StaticFileHandler, {"path": ".","default_filename": "login.html"}),
])

if __name__ == "__main__":
	application.listen(81,"0.0.0.0")
	tornado.ioloop.IOLoop.instance().start()
	
