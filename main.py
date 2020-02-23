
'''
                                                                    
88,dPYba,,adPYba,   ,adPPYba,  8b,dPPYba,   ,adPPYb,d8  ,adPPYba,   
88P'   "88"    "8a a8"     "8a 88P'   `"8a a8"    `Y88 a8"     "8a  
88      88      88 8b       d8 88       88 8b       88 8b       d8     
88      88      88 "8a,   ,a8" 88       88 "8a,   ,d88 "8a,   ,a8"  
88      88      88  `"YbbdP"'  88       88  `"YbbdP"Y8  `"YbbdP"'   
                                            aa,    ,88              
                                             "Y8bbdP"  

'''                                             


#Importaciones
from flask import Flask, request
from pymongo import MongoClient
from bson.json_util import dumps

from Src.create import *

#Inicialización APP:

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello, World!"

@app.route('/user/create/<username>')
def user(username):
    return createUser(username)

@app.route('/chat/create/')
def chat():
    usernames = request.args.get('usernames')
    usernames = "".join(usernames)
    usernames = usernames.split(",")
    arrayUsers = [element for element in usernames]
    return createChat(arrayUsers)

@app.route('/chat/<chat_id>/adduser')
def AddingUser(chat_id):
    username = request.args.get('username')
    username = "".join(username)
    username = username.split(",")
    arrayUsers = [element for element in username]
    return addUser(chat_id, arrayUsers)

@app.route('/chat/<chat_id>/addmessage', methods=['POST'])
def AddingMessage(chat_id):
    username = request.args.get('username')
    text = dict(request.json)
    body = text["text"]
    bodyDef = []
    body = bodyDef.append(body)
    return addMessage(chat_id, username, bodyDef)

@app.route('/chat/<chat_id>/list')
def getList(chat_id):
    simplePet = request.args.get('simple')
    return getMessages(chat_id, param=simplePet)

@app.route('/chat/<chat_id>/sentiment')
def getSentiment(chat_id):
    return getSentiments(chat_id)


app.run("0.0.0.0", 4500, debug=True)