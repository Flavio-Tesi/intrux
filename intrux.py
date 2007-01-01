import tornado.httpserver
import tornado.ioloop
import tornado.web
import json
import db_query
import datetime

class execute(tornado.web.RequestHandler):
	def get(self):
		if self.get_argument('cmd')=="read_users":
			self.write(json.dumps(db_query.read_users()))
		elif self.get_argument('cmd')=="read_lights":
			print db_query.read_lights()
			self.write(json.dumps(db_query.read_lights()))
		elif self.get_argument('cmd')=="change_light":
			i = int(self.get_argument('id'))
			db_query.change_light(i)
		elif self.get_argument('cmd')=="set_usercode":
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
		elif self.get_argument('cmd')=="temp_room":
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
		elif self.get_argument('cmd')=="read_rooms":
			self.write(json.dumps(db_query.read_rooms()))
			
		
application = tornado.web.Application([
	(r"/execute", execute),
	(r"/(.*)", tornado.web.StaticFileHandler, {"path": ".","default_filename": "index.html"}),
])

if __name__ == "__main__":
	application.listen(80,"0.0.0.0")
	tornado.ioloop.IOLoop.instance().start()
