import tornado.httpserver
import tornado.ioloop
import tornado.web
import json
import db_query

class execute(tornado.web.RequestHandler):
	def get(self):
		if self.get_argument('cmd')=="read_users":
			self.write(json.dumps(db_query.read_users()))
		elif self.get_argument('cmd')=="read_lights":
			self.write(json.dumps(db_query.read_lights()))
		elif self.get_argument('cmd')=="change_light":
			i = int(self.get_argument('id'))
			db_query.change_light(i)
		elif self.get_argument('cmd')=="set_usercode":
			i = int(self.get_argument('id'))
			if self.get_argument('pwd0')=='0':
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
			
		
application = tornado.web.Application([
	(r"/execute", execute),
	(r"/(.*)", tornado.web.StaticFileHandler, {"path": ".","default_filename": "index.html"}),
])

if __name__ == "__main__":
	application.listen(80,"0.0.0.0")
	tornado.ioloop.IOLoop.instance().start()
