from flask import Flask,render_template,request,session,redirect,url_for
from flask_socketio import SocketIO, emit, send, join_room, leave_room
import users,utility,messages
from utility import User

app = Flask(__name__)

app.secret_key = "defeegfrwgerrgisubug"
sock = SocketIO(app)


class Flash:
    WARN = "warn"
    SUCCESS = "success"
    ALERT = "alert"
    def __init__(self,msg,type_) -> None:
        self.msg = msg
        self.type = type_


# sign up and login system

@app.route("/",methods=["GET","POST"])
def index():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        img = request.files.get("img")
    
        if username and password:
            if not users.cheack_username(username):
                imgPath = utility.saveImage(img)
                if not imgPath:
                    flash = Flash("chose image type (png or jpg) please!",Flash.WARN)
                    return render_template("index.html", flash = flash)
                users.add(username,password,None,imgPath)
                flash = Flash("sign up seccessfully!",Flash.SUCCESS)
                return redirect(url_for("login"))
            else:
                flash = Flash("username is already exists! choose another username",Flash.WARN)
                return render_template("index.html", flash = flash)
        else:
            flash = Flash("Fill All the Inputs , please !",Flash.WARN)
            return render_template("index.html", flash = flash)
    return render_template("index.html")

@app.route("/login",methods=["GET","POST"])
def login():
    if session.get("user"):
        return redirect(url_for("profile"))
    if request.method == "POST":
        # cheack users if exists
        username = request.form.get("username")
        password = request.form.get("password")
        user = users.user_exists(username,password)
        if user:
            session["user"] = (user[0],user[1],user[4])
            return redirect(url_for("profile"))

    return render_template("login.html")

@app.route("/logout")
def logout():
    if session.get("user"):
        session.clear()
        return redirect(url_for("login"))

@app.route("/profile")
def profile():
    if session.get("user"):
        user = session.get("user")
        id_ = user[0]
        user = users.select(id_) # (id,username,password,sid,img)
        user = User(id_,user[1],user[4])
        my_msgs = utility.find_last_msgs(user.id) # exp [( User(2, ali), 'hello back ali' ), ( User(3, sami), 'hello hammody i am sami') ]
        return render_template("profile.html",user = user,my_msgs = my_msgs)
    return render_template("login.html")

@app.route("/profile/<int:user_id>")
def profile_msgs(user_id):
    if session.get("user"):
        user = session.get("user")
        id_ = user[0]
        actual_msgs = messages.select(id_,user_id)
        user = users.select(id_) # (id,username,password,sid,img)
        user = User(id_,user[1],user[4])
        my_msgs = utility.find_last_msgs(user.id) # exp [( User(2, ali), 'hello back ali' ), ( User(3, sami), 'hello hammody i am sami') ]
        return render_template("profile_msgs.html",user = user,my_msgs = my_msgs,actual_msgs=actual_msgs,other_user_id = user_id)
    return render_template("login.html")

@sock.on("conn")
def conn(data):
    user = session.get("user")
    user = User(user[0],user[1],user[2])
    print(request.sid)
    print(data)
    users.update_sid(request.sid,user.id)

@sock.on("msg")
def msg(data):
    print(data)
    # {sender: '1', reciever: '2', msgBody: 'dfegrhtjyuki,l,ukytjrerherhte'}
    messages.add(data['msgBody'],int(data['sender']),int(data['reciever']))
    other_user_data = users.select(int(data['reciever'])) # get the sid
    print("other_user_data : ",other_user_data[3])
    if(other_user_data[3]):
        sid = other_user_data[3]
        sender_data = users.select(int(data['sender']))
        sender_username = sender_data[1]
        data = {"msgBody":data['msgBody'],"username":sender_username}
        emit("msg",data,room = sid)
    # else:
    #     sender_data = users.select(int(data['sender']))
    #     sender_username = sender_data[1]
    #     data = {"msgBody":data['msgBody'],"username":sender_username}
    #     emit("msg",data,broadcast = False)


@sock.on("disconn")
def disconn(id_):
    # make the sid column empty for disconnected user
    print("disconnected",id_)
    users.update_sid(None,id_)



















if __name__ == "__main__":
    users.createTable()
    messages.createTable()
    sock.run(app,debug=True)
    
















