#coding:utf-8
from mimetypes import common_types
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


def getRoomlist():
    
    command = "select room.roomid,room.roomname,room.created_time,room.owner_id,user.username,room.members from room,user where room.owner_id == user.userid"
    cursor = conn.execute(command)
    roomlist = list(cursor.fetchall())
    # print(roomlist)
    return roomlist

def getRoominfo(room):
    command = "select * from room where roomid = %d" % (room)
    cursor = conn.execute(command)
    if cursor.fetchone() is None:
        return None #房间号不存在
    command = "select room.roomid,room.roomname,room.created_time,room.owner_id,user.username,room.members from room,user where room.roomid = %d and room.owner_id == user.userid" % (room)
    cursor= conn.execute(command)
    roominfo = list(cursor.fetchone())
    return roominfo
def check_room(roomname):
    if "&" in roomname:
        return True
    command = "select roomname from room where roomname = '%s' " %(roomname)
    cur.execute(command)
    if cur.fetchall():
        return True
    return False
def get_friends(username):
    command = "select user.friends from user where user.username = '%s' "%(username)
    cursor= conn.execute(command)
    friends = cursor.fetchone()[0]
    return friends

def get_users():
    command = "select user.username from user"
    cursor = conn.execute(command)
    user_list = [x[0] for x in cursor.fetchall()]
    return user_list