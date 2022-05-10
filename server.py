import tornado.web
import tornado.ioloop
import tornado.httpserver
import tornado.options
import os.path
import sqlite3
import datetime
import time
from tornado.web import RequestHandler
from tornado.options import define, options
from tornado.websocket import WebSocketHandler
from login import LoginHandler,LogoutHandler
from register import RegisterHandler
from chatroom import ChatHandler,ChatroomHanlder,CreateroomHandler
from longpolling import LongPollingHandler
from user import ModifyHandler,AddHandler

define("port", default=8200, help="run on given port", type=int)

class Application(tornado.web.Application):
	def __init__(self):
		handlers = [(r'/login', LoginHandler),
					(r'/logout',LogoutHandler),
					(r'/',LoginHandler),
                    (r'/register',RegisterHandler),
					(r'/chatroom',ChatroomHanlder),
					(r'/create',CreateroomHandler),
					(r'/room/\d*',ChatHandler),
					(r'/longpolling',LongPollingHandler),
					(r'/modify',ModifyHandler),
					(r'/add',AddHandler)
					]
		settings = dict(
					cookie_secret =
					"WMLs5RFoTjKBjuDFLH7gX1S+ArUr20cWkVmC1m+DcNs=",
					template_path =
					os.path.join(os.path.dirname(__file__), "templates"),
					static_path =
					os.path.join(os.path.dirname(__file__), "static"),
					)
		tornado.web.Application.__init__(self, handlers, **settings)

if __name__ == "__main__":
	tornado.options.parse_command_line()
	http_server = tornado.httpserver.HTTPServer(Application())
	http_server.listen(options.port)
	print('http://localhost:8200')
	tornado.options.parse_command_line()
	tornado.ioloop.IOLoop.instance().start()
