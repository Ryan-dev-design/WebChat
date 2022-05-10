import sqlite3

def init():
    conn=sqlite3.connect("chatroom.db")
    cur=conn.cursor()

    command = """
    BEGIN;
    CREATE TABLE IF NOT EXISTS user(
        "userid" integer PRIMARY KEY AUTOINCREMENT,
        "username" varchar(25) NOT NULL, 
        "password" varchar(50) NOT NULL,
        "friends" varchar(9999) NOT NULL,
        "registed_time" datetime NOT NULL,
        "reverse1" integer DEFAULT NULL,
        "reverse2" varchar(50) DEFAULT NULL,
        UNIQUE("username") 
    );

    CREATE TABLE IF NOT EXISTS room(
        "roomid" integer PRIMARY KEY AUTOINCREMENT,
        "roomname" varchar(50) NOT NULL,
        "created_time" datetime NOT NULL,
        "owner_id" integer NOT NULL,
        "members" varchar(999) NOT NULL,
        UNIQUE("roomname")
    );

    CREATE TABLE IF NOT EXISTS message(
        "msgid" integer PRIMARY KEY AUTOINCREMENT,
        "roomid" integer NOT NULL,
        "username" varchar(25) NOT NULL,
        "msg" varchar(500) NOT NULL,
        "created_time" datetime DEFAULT NULL,
        "reverse1" varchar(50) DEFAULT NULL
    );
    COMMIT;
    """

    try:
        cur.executescript(command)
        conn.commit()
    except Exception as e:
        print(e)

    cur.close()
    conn.close()

if __name__ == "__main__":
    init()
