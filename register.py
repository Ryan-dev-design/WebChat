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
class RegisterHandler(tornado.web.RequestHandler):

    def check_name(self,username):#check if the username is used
        command="select * from user where username = '%s'" %(username)
        cur.execute(command)
        
        if cur.fetchall():
            return True#if the username is used
        return False

    def get(self):
        self.render('register.html',Error=False)

    def post(self):
        username=self.get_argument("username")
        password=self.get_argument("password")
        password2=self.get_argument("password2")
        if not password == password2:
            self.write("please enter the same password!")
            self.render("register.html",Error=True)
        
        if self.check_name(username=username):
            self.write("the name has been registered! Please try another name.")
            self.render('register.html',Error=True)
        else:
            command="insert into user (username, password, registed_time, friends) values ('%s','%s', datetime('now'),'%s')"%(username,password,"")
            conn.execute(command)
            conn.commit()
            self.write("register successfully!")
            time.sleep(1)
            self.set_secure_cookie(name="username",value=username,expires_days=1)
            cookie_user=self.get_argument("username")
            self.render("login.html",cookieUser=cookie_user)


if __name__ == "__main__":
    define(name="port",default=8200,help="run on given port", type=int)
    tornado.options.parse_command_line()
    app = tornado.web.Application(
		handlers=[(r'/register', RegisterHandler)],
		template_path=os.path.join(os.path.dirname(__file__), "templates")
		)
    http_server=tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

