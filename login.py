import tornado.web
import tornado.ioloop
import tornado.httpserver
import tornado.options

import os.path
import sqlite3
import time

from tornado.options import define, options

conn = sqlite3.connect('chatroom.db')
cur  = conn.cursor()

class LoginHandler(tornado.web.RequestHandler):
    def user_check(self,username,password):
        command = "select * from user where username = '%s' and password = '%s' " %(username, password)
        cur.execute(command)
        if cur.fetchall():
            return True
        return False

    def get(self):
        cookie_user = self.get_secure_cookie("username")
        self.render('login.html',cookieUser=cookie_user,Error=False)
    def post(self):
        username = self.get_argument('username')
        password = self.get_argument('password')
        if self.user_check(username,password):# password is correct!
            self.set_secure_cookie(name="username", value=username,expires_days=1)
            # the login expires after one day
            cookie_user = self.get_argument('username')
            self.render('login.html', cookieUser=cookie_user,Error=False)
        else:#password is incorrect!
            self.render('login.html',cookieUser=None,Error=True)


class LogoutHandler(tornado.web.RequestHandler):
    def get(self):
        self.clear_all_cookies()
        # time.sleep(1)
        self.redirect("/login")

    
if __name__ == "__main__":
    define(name="port",default=8200,help="run on given port", type=int)
    tornado.options.parse_command_line()
    app = tornado.web.Application(
		handlers=[(r'/login', LoginHandler),
				  (r'/logout', LogoutHandler)],
		template_path=os.path.join(os.path.dirname(__file__), "templates"),
		cookie_secret="WMLs5RFoTjKBjuDFLH7gX1S+ArUr20cWkVmC1m+DcNs="
		)
    http_server=tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

    