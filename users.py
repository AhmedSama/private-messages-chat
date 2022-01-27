import sqlite3


def createTable():
    conn = sqlite3.connect("data.db")
    cur = conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS users (
        username varchar(20) not null,
        pwd varchar(50) not null,
        sid varchar(100) ,
        img varchar(30) not null DEFAULT '/images/default.png'
    )
    """)
    conn.commit()
    cur.close()
    conn.close()

def add(username, pwd, sid ,img):
    conn = sqlite3.connect("data.db")
    cur = conn.cursor()
    cur.execute("INSERT INTO users (username,pwd,sid,img) VALUES (?,?,?,?)",(username, pwd, sid ,img))
    conn.commit()
    cur.close()
    conn.close()

def update_sid(sid,id_):
    conn = sqlite3.connect("data.db")
    cur = conn.cursor()
    cur.execute("UPDATE users SET sid = ? WHERE users.rowid = ?",( sid ,id_))
    conn.commit()
    cur.close()
    conn.close()



# find all users that i sent them a message
def find_users_i_sent_message(id_):
    conn = sqlite3.connect("data.db")
    cur = conn.cursor()
    cur.execute("SELECT msgs.sender,msgs.reciever, users.username, users.img,msgs.msg FROM msgs join users on msgs.sender = users.rowid  WHERE msgs.sender = ? or msgs.reciever = ?",(id_,id_))
    conn.commit()
    data = cur.fetchall()
    cur.close()
    conn.close()
    # if user not exists it returns None
    return data





def cheack_username(username):
    conn = sqlite3.connect("data.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM users where users.username = ?",(username,))
    conn.commit()
    data = cur.fetchone()
    cur.close()
    conn.close()
    # if user not exists it returns None
    return data

def user_exists(username,password):
    conn = sqlite3.connect("data.db")
    cur = conn.cursor()
    cur.execute("SELECT rowid,* FROM users where users.username = ? AND users.pwd = ?",(username,password))
    conn.commit()
    data = cur.fetchone()
    cur.close()
    conn.close()
    # if user not exists it returns None
    return data

def show():
    conn = sqlite3.connect("data.db")
    cur = conn.cursor()
    cur.execute("SELECT rowid,* FROM users")
    conn.commit()
    data = cur.fetchall()
    cur.close()
    conn.close()
    return data

def select(id_):
    conn = sqlite3.connect("data.db")
    cur = conn.cursor()
    cur.execute("SELECT rowid,* FROM users WHERE users.rowid = ? ",(id_,))
    conn.commit()
    data = cur.fetchone()
    cur.close()
    conn.close()
    return data

def delete(id_):
    conn = sqlite3.connect("data.db")
    cur = conn.cursor()
    cur.execute("DELETE FROM users WHERE users.rowid = ? ",(id_,))
    conn.commit()
    cur.close()
    conn.close()


# add("ahmed","123",None,"pathtoimg")

# add("ali","efef",None,"pathtoimg")
# add("sami","efef",None,"pathtoimg")
# add("jawad","efef",None,"pathtoimg")
# add("maitham","efef",None,"pathtoimg")

# print(find_users_i_sent_message(1))
# print(select(1))







