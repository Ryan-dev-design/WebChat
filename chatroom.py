#coding:utf-8
import tornado.web
import tornado.ioloop
import tornado.httpserver
import tornado.options

import os.path
import sqlite3
import time
from tornado.escape import json_encode
import tornadoredis
from tornado.options import define, options

conn = sqlite3.connect('chatroom.db')
cur  = conn.cursor()

c = tornadoredis.Client()
c.connect()


from get import get_friends,getRoominfo,getRoomlist,check_room
# 显示聊天室
class ChatroomHanlder(tornado.web.RequestHandler):

    def get_current_user(self):
        return self.get_secure_cookie("username")

    def get(self):
        cookie_user=self.get_current_user()
        roomlist_=getRoomlist()
        print(roomlist_)
        roomlist=[]#存放当前用户所在的聊天室
        private=[]#存放私聊聊天室
        for room in roomlist_:
            if "&" in room[1]:
                members = room[5].split(",")
                if cookie_user in members:
                    if members[0] == cookie_user:
                        friend = members[1]
                    else:
                        friend = members[0]
                    room = room+(friend,)
                    private.append(room)
            else:
                members = room[5].split(",")#members中用','分割用户名
                if room[4] == cookie_user or cookie_user in members:
                    roomlist.append(room)
        roomlist = tuple(roomlist)
        private = tuple(private)
        print(private)
        if cookie_user:
            self.render('chatroom.html', cookieUser=cookie_user,Error=False,roomlist=roomlist,private=private)
        else:
            self.render('login.html',cookieUser=None,Error=False)
        

class CreateroomHandler(tornado.web.RequestHandler):

    def get(self):
        cookie_user = self.get_secure_cookie("username")
        friends_ = get_friends(cookie_user)#由逗号分隔的好友列表
        if friends_ == None:
            friends = ""
        else:
            friends = tuple(friends_.split(","))
        if cookie_user:
            self.render('create.html',cookieUser=cookie_user,friends=friends,Error=False)
        else:
            self.render('login.html',cookieUser=None,Error=False)
    def post(self):
        roomname = self.get_argument('roomname')
        members = self.get_argument("members")
        username = self.get_secure_cookie('username')
        print(members)
        if check_room(roomname=roomname):#检查是否合法
            self.render('create.html', cookieUser=username, Error=True)
            return 
        command = "select userid from user where username = '%s'" %(username)
        cursor = conn.execute(command)
        for row in cursor:
            userid = row[0]
        command = "insert into room (roomname, created_time, owner_id,members) values('%s', datetime('now'), %d,'%s')" %(roomname,userid,members)
        conn.execute(command)
        conn.commit()
        self.redirect("/chatroom")

class ChatHandler(tornado.web.RequestHandler):

    def get(self):
        uri_list = self.request.uri.split('/')
        roomid = int(uri_list[-1])
        self.set_secure_cookie("roomid", str(roomid),1)
        cookie_user = self.get_secure_cookie("username")
        if cookie_user:
            roominfo = getRoominfo(roomid)
            if roominfo is None:
				#跳转404
                self.render("404err.html")
			#成功合法跳转某聊天房
            else:
                command = "select username,msg,created_time from message where roomid = %d order by msgid desc limit 100" % (roomid)
                cursor = conn.execute(command)
				#最近50条聊天记录
                msginfoList = list(cursor.fetchall())
                msginfoList.reverse()
                self.render('chat.html', cookieUser=cookie_user, roominfo=roominfo, msginfo=msginfoList)
        else:#跳转登陆界面
            self.render('login.html', cookieUser=None, Error = False)
    @tornado.web.asynchronous
    def post(self):
        username = self.get_secure_cookie("username")
        msg = self.get_argument("msg")
        data = json_encode({'name':username, 'msg':msg})
        roomchannel = str(self.get_secure_cookie('roomid'))
        command = "insert into message(roomid,username,msg,created_time) values(%d,'%s','%s',datetime('now'))" % (int(roomchannel),username,msg)
        conn.execute(command)
        conn.commit()

		#收到将消息publish到Redis
		#print data
        c.publish(roomchannel, data)
        self.write(json_encode({'result':True}))
        self.finish()