import sqlite3


def createTable():
    conn = sqlite3.connect("data.db")
    cur = conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS msgs (
        msg text not null,
        sender integer not null,
        reciever integer not null,
        readed bit default '0'
    )
    """)
    conn.commit()
    cur.close()
    conn.close()


def add(msg,sender,reciever):
    conn = sqlite3.connect("data.db")
    cur = conn.cursor()
    cur.execute("INSERT INTO msgs (msg,sender,reciever) VALUES (?,?,?)",(msg,sender,reciever))
    conn.commit()
    cur.close()
    conn.close()

def show():
    conn = sqlite3.connect("data.db")
    cur = conn.cursor()
    cur.execute("SELECT rowid,* FROM msgs")
    conn.commit()
    data = cur.fetchall()
    cur.close()
    conn.close()
    return data

def select(sender,reciever):
    conn = sqlite3.connect("data.db")
    cur = conn.cursor()
    cur.execute("SELECT users.username,msgs.msg FROM msgs join users on users.rowid = msgs.sender where (msgs.sender = ? and msgs.reciever = ?) or (msgs.reciever = ? and msgs.sender = ?) order by msgs.rowid desc",(sender,reciever,sender,reciever))
    conn.commit()
    data = cur.fetchall()
    cur.close()
    conn.close()
    return data

def delete(id_):
    conn = sqlite3.connect("data.db")
    cur = conn.cursor()
    cur.execute("DELETE FROM msgs WHERE msgs.rowid = ? ",(id_,))
    conn.commit()
    cur.close()
    conn.close()


# add("ahmed","efef","ferg9dfhibui","pathtoimg")

# add("ali","efef","ferg9dfhibui","pathtoimg")
# add("sami","efef","ferg9dfhibui","pathtoimg")
# add("jawad","efef","ferg9dfhibui","pathtoimg")
# add("maitham","efef","ferg9dfhibui","pathtoimg")

# print(select(1))


# add("hello i am ahmed",1,2)
# add("hello i am ali",2,1)
# add("hello sami i am ahmed",1,3)
# add("hello hammody i am sami",3,1)


# add("hello back ali",1,2)


# print(select(1,2))

