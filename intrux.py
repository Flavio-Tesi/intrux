import tornado.httpserver
import tornado.ioloop
import tornado.web
import json
import datetime
import time
import threading
import db_query
import daisy_function
import comandi_shell
import screen_read
import rfid
import send_email

class ThreadTemp(threading.Thread):														#thread per log temperature
	def run(self):
		while True:
			x = datetime.datetime.now()
			id_room = 1
			val = int(comandi_shell.leggi_temperatura())
			dat = datetime.datetime.strftime(x,"%Y-%m-%d")
			ora = datetime.datetime.strftime(x,"%H:%M:%S")
			db_query.set_temperature(id_room, val, dat, ora)
			time.sleep(1800)
ttemperature = ThreadTemp()
ttemperature.daemon = True
ttemperature.start()

class ThreadRecordCam(threading.Thread):												#thread per record cam
	def __init__(self):
		super(ThreadRecordCam, self).__init__()
		self._stop = threading.Event()
	def stop(self):
		self._stop.set()
	def run(self):
		comandi_shell.on_record()
treccam = ThreadRecordCam()
treccam.daemon = True

class ThreadCam(threading.Thread):														#thread per cam
	def __init__(self):
		super(ThreadCam, self).__init__()
		self._stop = threading.Event()
	def stop(self):
		self._stop.set()
	def run(self):
		comandi_shell.on_cam_640_480()	
tcam = ThreadCam()
tcam.daemon = True

class ThreadCamHD(threading.Thread):													#thread per cam hd
	def __init__(self):
		super(ThreadCamHD, self).__init__()
		self._stop = threading.Event()
	def stop(self):
		self._stop.set()
	def run(self):
		comandi_shell.on_cam_1280_720()
tcamhd = ThreadCamHD()
tcamhd.daemon = True

class ThreadAllarme(threading.Thread):													# thread allarme
	def __init__(self):
		super(ThreadAllarme, self).__init__()
		self._stop = threading.Event()
	def stop(self):
		self._stop.set()
	def stopped(self):
		return self._stop.isSet()					
	def run(self):
		allarm = "disattivato"
		while not(self.stopped()):
			x = daisy_function.allarme(allarm)
			if x == "ALLARME":
				allarm = "attivato"
			time.sleep(0.1)					
tallarme = ThreadAllarme()
tallarme.daemon = True
tallarme.stop()

class ThreadLuci(threading.Thread):														#thread per luci
	def run(self):
		a = True
		b = True
		c = True
		d = True
		while True:
			x = daisy_function.luci(a,b,c,d)
			if x == "10":
				a = False
			elif x == "11":
				a = True
			if x == "20":
				b = False
			elif x == "21":
				b = True
			if x == "30":
				c = False
			elif x == "31":
				c = True
			if x == "40":
				d = False
			elif x == "41":
				d = True		
			time.sleep(0.1)	
tluci = ThreadLuci()
tluci.daemon = True
tluci.start()

class ThreadScreen(threading.Thread):													#thread per schermo
	def __init__(self):
		super(ThreadScreen, self).__init__()
		self._stop = threading.Event()
	def stop(self):
		self._stop.set()
	def stopped(self):
		return self._stop.isSet()					
	def run(self):
		pacchetto = ""
		lista = []
		while True:
			lettura = screen_read.function()
			
			if lettura != None:
				pacchetto="".join([pacchetto,lettura])

			# GLI ACK PER IL GOTO_FORM
			if pacchetto != "":
				if pacchetto[0] == "\x06":
					pacchetto = ""
				
			if len(pacchetto) == 6:			
				spacchettamento = screen_read.spacchetta(pacchetto)
				
				if spacchettamento == "OK":
					numero_codice = pacchetto[-2]
					numero_bottone = pacchetto [2]
					comando = pacchetto [1]

					if numero_codice == "\x08":
						
						x = screen_read.verifica(lista)
						if x == 1:
							screen_read.goto_form(1)
							time.sleep(0.1)
							pacchetto = ""		
							daisy_function.stop_allarme()
							tallarme.stop()
							daisy_function.luce_allarme_disattivato()	
						elif x == 2:
							screen_read.goto_form(2)	
							time.sleep(0.1)
							pacchetto = ""			
							daisy_function.stop_allarme()
							tallarme.stop()
							daisy_function.luce_allarme_disattivato()	
							orario = datetime.datetime.strftime(datetime.datetime.now(),"%H:%M")	
							if not((orario > '10:00') & (orario < '21:00')):
								send_email.invia_email_rfid_utente()	
					elif numero_codice == "\x3c":
						if len(lista)>0:
							del lista [-1]
					elif (comando == "\x06") & (numero_bottone == "\x00"):
						tallarme.__init__()
						tallarme.start()
						daisy_function.luce_allarme_attivato()
						pacchetto = ""
						del lista[0:99] 
						screen_read.goto_form(0)
						time.sleep(0.1)
						pacchetto = ""		
					elif (comando == "\x06") & (numero_bottone == "\x01"):
						screen_read.goto_form(1)
						time.sleep(0.1)
						pacchetto = ""
						del lista[0:99] 
					elif (comando == "\x06") & (numero_bottone == "\x02"):
						tallarme.__init__()
						tallarme.start()
						daisy_function.luce_allarme_attivato()
						pacchetto = ""
						del lista[0:99] 
						screen_read.goto_form(0)
						time.sleep(0.1)
						pacchetto = ""		
					else:
						lista.append (numero_codice)
				pacchetto = ""
			
		time.sleep(0.5)	
tschermo = ThreadScreen()
tschermo.daemon = True
tschermo.stop()
tschermo.start()

class ThreadRFID(threading.Thread):														#thread per rfid
	def run(self):
		while True:
			x = rfid.function()
			if x == "admin": 
				if tallarme.stopped():
					tallarme.__init__()
					tallarme.start()
					daisy_function.luce_allarme_attivato()
					screen_read.goto_form(0)
					time.sleep(0.1)
				else:
					daisy_function.stop_allarme()
					tallarme.stop()
					daisy_function.luce_allarme_disattivato()
					screen_read.goto_form(1)
					time.sleep(0.1)		
			if x == "user":
				if tallarme.stopped():
					tallarme.__init__()
					tallarme.start()
					daisy_function.luce_allarme_attivato()
					screen_read.goto_form(0)
					time.sleep(0.1)
					pacchetto = ""		
				else:
					daisy_function.stop_allarme()
					tallarme.stop()
					daisy_function.luce_allarme_disattivato()
					orario = datetime.datetime.strftime(datetime.datetime.now(),"%H:%M")
					if not((orario > '10:00') & (orario < '21:00')):
						send_email.invia_email_rfid_utente()
					screen_read.goto_form(2)
					time.sleep(0.1)
					pacchetto = ""		
trfid = ThreadRFID()
trfid.daemon = True
trfid.start()


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
			tallarme.stop()
		elif self.get_argument('cmd')=="start_allarme":									#avvia allarme	
			if tallarme.stopped():
				tallarme.__init__()
				tallarme.start()
		elif self.get_argument('cmd')=="on_cam":										#accendi cam a bassa risoluzione
			comandi_shell.off_cam()
			time.sleep(1)
			tcam.__init__()
			tcam.start()	
			time.sleep(2)
		elif self.get_argument('cmd')=="on_cam_hd":										#accendi cam a alta risoluzione
			comandi_shell.off_cam()
			time.sleep(1)
			tcamhd.__init__()
			tcamhd.start()
			time.sleep(2)
		elif self.get_argument('cmd')=="off_cam":										#spegni cam
			tcam.stop()
			tcamhd.stop()
			comandi_shell.off_cam()
		elif self.get_argument('cmd')=="record_video":									#record cam
			tcam.stop()
			tcamhd.stop()
			comandi_shell.off_cam()	
			treccam.__init__()
			treccam.start()
		elif self.get_argument('cmd')=="stop_record_video":								#stop record cam
			treccam.stop()
			comandi_shell.off_record()
			

		
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
	
