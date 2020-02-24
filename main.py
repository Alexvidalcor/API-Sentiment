
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
    output = createUser(username)
    return f"Creado {username} con index {output}"

@app.route('/chat/create/')
def chat():
    usernames = request.args.get('usernames')
    usernames2 = "".join(usernames)
    usernames3 = usernames2.split(",")
    arrayUsers = [element for element in usernames3]
    output = createChat(arrayUsers)
    return f"Creado chat {output} con {usernames}"

@app.route('/chat/<chat_id>/adduser')
def AddingUser(chat_id):
    username = request.args.get('username')
    username2 = "".join(username)
    username3 = username2.split(",")
    arrayUsers = [element for element in username3]
    output = addUser(chat_id, arrayUsers)
    return f"{username} se ha unido en chat {output}"

@app.route('/chat/<chat_id>/addmessage', methods=['POST'])
def AddingMessage(chat_id):
    username = request.args.get('username')
    text = dict(request.json)
    body = text["text"]
    bodyDef = []
    body = bodyDef.append(body)
    output = addMessage(chat_id, username, bodyDef)
    return f"Añadido mensaje al chat {chat_id}, {username}: {bodyDef}"
    
@app.route('/chat/<chat_id>/list')
def getList(chat_id):
    simplePet = request.args.get('simple')
    return getMessages(chat_id, simple=simplePet)

@app.route('/chat/<chat_id>/sentiment')
def getSentiment(chat_id):
    alternative = request.args.get('alter')
    return getSentiments(chat_id,alternative)

@app.route('/user/<user_id>/recommend')
def recomendator(user_id):
    return getSentiments(user_id)

#COSAS PENDIENTES: DEFINIR SI GUARDAR JSON EN LOS ENDPOINTS DE JSON
app.run("0.0.0.0", 4500, debug=True)