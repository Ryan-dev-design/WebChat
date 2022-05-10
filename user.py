#coding:utf-8
from lib2to3.pgen2.token import tok_name
import tornado.web
import tornado.ioloop
import tornado.httpserver
import tornado.options

import os.path
import sqlite3
import datetime
import time
from get import get_friends,getRoominfo,getRoomlist,get_users
from tornado.options import define, options
conn = sqlite3.connect("chatroom.db")
cur = conn.cursor()
class ModifyHandler(tornado.web.RequestHandler):
    def check_user(self, username, password):
        command = "select * from user where username = '%s' and password = '%s' " %(username, password)
        cur.execute(command)
        if cur.fetchall():
            return True
        return False

    def get(self):
        cookie_user = self.get_secure_cookie("username")
        if cookie_user is None:
            self.redirect('/login')
        self.render('modify.html',cookieUser=cookie_user,Error=False)
    
    def post(self):
        username = self.get_secure_cookie("username")
        password0 = self.get_argument("password0")
        password = self.get_argument("password")
        password2 =self.get_argument("password2")
        if not self.check_user(username,password0):
            self.render('modify.html',cookieUser=username,Error=True)
        if password != password2:
            self.write("两次密码输入不一致")
            print(password,password2)
            self.render('modify.html',cookieUser=username,Error=False)
        command = "update user set password = '%s' where username = '%s'"%(password,username)
        conn.execute(command)
        conn.commit()
        self.write("successfully modified")
        self.redirect('/logout')

class AddHandler(tornado.web.RequestHandler):
    def get(self):
        cookie_user = self.get_secure_cookie("username")
        users_=get_users()
        friends_ = get_friends(cookie_user)#由逗号分隔的好友列表
        if friends_ == None:
            friends = [cookie_user,]
        else:
            friends = tuple(friends_.split(",")+[cookie_user,])
        if users_ == None:
            users = ""
        else:
            users = tuple([x for x in users_ if x not in friends])
        if cookie_user:
            self.render('add.html',cookieUser=cookie_user,friends=friends,users=users)
        else:
            self.render('login.html',cookieUser=None,Error=False)

    def post(self):
        cookie_user = self.get_secure_cookie("username")
        added_friends = self.get_argument("added")
        friends = get_friends(cookie_user)#由逗号分隔的好友列表
        if friends == None:
            friends = ""
        new_friends = friends+','+added_friends
        command = "update user set friends ='%s' where username ='%s'"%(new_friends,cookie_user)
        conn.execute(command)
        #新增好友建立私聊聊天室
        added_list = added_friends.split(",")
        for friend in added_list:
            if cookie_user < friend:#大的在前,确保一致性
                roomname = cookie_user+"&"+friend
            else:
                roomname = friend + "&" + cookie_user
            members = cookie_user+","+friend
            command = "select userid from user where username = '%s'" %(cookie_user)
            cursor = conn.execute(command)
            for row in cursor:
                userid = row[0]
            print(userid)
            command = "insert into room (roomname, created_time, owner_id,members) values('%s', datetime('now'), %d,'%s')" %(roomname,userid,members)#用owner_id = 0标记私聊聊天室
            conn.execute(command)
            friends_of_friend = get_friends(friend)
            new_friends_of_friend = friends_of_friend +','+cookie_user
            command = "update user set friends ='%s' where username ='%s'"%(new_friends_of_friend,friend)
            conn.execute(command)
        conn.commit()
        self.write("successfully added!")
        self.redirect("/add")
if __name__ == '__main__':
	define("port", default=8200, help="run on given port", type=int)
	tornado.options.parse_command_line()
	app = tornado.web.Application(
		handlers=[(r'/modify', ModifyHandler)],
		template_path=os.path.join(os.path.dirname(__file__), "templates")
		)
	http_server = tornado.httpserver.HTTPServer(app)
	http_server.listen(options.port)
	tornado.ioloop.IOLoop.instance().start()