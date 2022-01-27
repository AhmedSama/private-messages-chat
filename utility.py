from os import path
from os.path import join
from random import randint
import users

absPath = path.dirname(path.realpath(__file__))

valid_file_extensions = ["png","jpg"]


class User:
    def __init__(self,id_,username,img) -> None:
        self.id = id_
        self.username = username
        self.img = img

    def __repr__(self) -> str:
        return f"User({self.id}, {self.username})"

def validFile(filename:str):
    fileExtension = filename.split(".")[-1]
    return fileExtension in valid_file_extensions

def changeFileName(filename):
    name,ext = [filename.split('.')[0], filename.split('.')[-1]]
    name += str(randint(1000,10000000))
    return name + "." + ext

def saveImage(img):
    if not img:
        return "/images/"+"default.png"
    imgName = img.filename
    if validFile(imgName):
        filename = changeFileName(imgName)
        img.save(join(absPath,"static","images",filename))
        return "/images/"+filename # the file path i need to store in users table 
    else: return None 



# the input like this [(1, 2, 'ahmed', 'pathtoimg', 'hello i am ahmed'), (2, 1, 'ali', 'pathtoimg', 'hello i am ali'), (1, 3, 'ahmed', 'pathtoimg', 'hello sami i am ahmed'), (3, 1, 'sami', 'pathtoimg', 'hello hammody i am sami'), (1, 4, 'ahmed', 'pathtoimg', 'hello test'), (1, 2, 'ahmed', 'pathtoimg', 'hello back ali')]
# return list of lists contain [(user1,'last msg'),(user2,'last msg')] where user is object of class User
def find_last_msgs(id_):
    final_data = []
    data = users.find_users_i_sent_message(id_)
    ids = makeIds(data,id_) # returns [(1, 2), (1, 3), (1, 4)] list of tubles where first one is the user id and the second is the other
    for element in ids:
        final_data.append(makeUser(data,element[0],element[1]))
    return final_data

# return list of ids exp : [(1,2),(1,3)] where the first id is the user id and the second is the other user
def makeIds(list_,id_):
    data = []
    user_id = None
    other_id = None
    for element in list_:
        if (element[0],element[1]) in data or (element[1],element[0]) in data:
            continue
        if(element[0] == id_):
            user_id = element[0]
            other_id = element[1]
        else:
            user_id = element[1]
            other_id = element[0]
        data.append((user_id,other_id))
    return data

def makeUser(list_,id_,other_id):
    last_one = None
    for elemnt in list_:
        if (elemnt[0] == id_ and elemnt[1] == other_id) or (elemnt[0] == other_id and elemnt[1] == id_):
            last_one = elemnt

    # last_one example  = (1, 2, 'ahmed', 'pathtoimg', 'hello back ali')
    last_msg = last_one[4]
    the_other_user_id = None
    if last_one[0] != id_:
        the_other_user_id = last_one[0]
    else:
        the_other_user_id = last_one[1]
    user_data = users.select(the_other_user_id) # returns (rowid,username,password,sid,img)
    user = User(user_data[0],user_data[1],user_data[4])
    return (user,last_msg)























