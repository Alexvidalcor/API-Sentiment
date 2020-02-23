from Src.idGenerator import *
from Src.finding import *
from Src.mongoThings import *
from Src.errorHandler import *

from bson.objectid import ObjectId
import json

# @jsonErrorHandler
def createUser(username):

    #Seleccionar Database
    db = pickDB()

    #Insertar PositionID
    idGenerated = idGenerator()
    db.insert_one({'Position':idGenerated, 'Username':username})

    #Devolver ChatID
    projection = {'Position':1}
    limit = 1
    sort = sort=list({'_id': -1}.items())
    lastId = db.find(projection=projection,sort=sort,limit=limit)
    calc = [element["Position"]for element in lastId][0]
    
    return dumps(int(calc))


def createChat(arrayUsers):

    #Seleccionar Database
    db = pickDB(method="Chats")

    #Insertar ChatID
    idGenerated = idGenerator(method="Chats")

    #Insertar Array de usuarios
    lengthArray = len(arrayUsers)
    userSearch = findThings(arrayUsers, length=lengthArray)
    db.insert({"Position":idGenerated, "idUsers":userSearch})

    #Devolver ChatID
    projection = {'Position':1}
    limit = 1
    sort = sort=list({'_id': -1}.items())
    lastId = db.find(projection=projection,sort=sort,limit=limit)
  
    calc = [element["Position"]for element in lastId][0]
    return dumps(int(calc))


def addUser(chat_id, array):

    #Seleccionar Database
    dbU = pickDB()
    dbC = pickDB(method="Chats")

    #Generamos o Localizamos UserID
    lengthArray = len(array)
    userSearch = findThings(array, length=lengthArray)

    #Localizamos el ID del chat para realizar el update
    idLocated = findThings(chat_id, method = "Chats", style="_id")

    #Comprobación de duplicados
    
    #Realizamos la inserción
    for element in userSearch:
        dbC.update({"_id":idLocated[-1]}, {"$addToSet":{"idUsers":element}})

    #Devolvemos el ID del chat 
    return dumps(int(chat_id))

    
def addMessage(chat_id, username, text):

    #Seleccionamos database
    db = pickDB(method="Chats")

    #Localizamos el ID del username introducido (falta raise cuando duplicados)
    lengthArray = len(username)
    username = username.split("%/&$")
    userSearch = findThings(username, length=lengthArray,create=False)
    userSearch = userSearch[-1]

    #Chequeo de usuarios existentes
    checkExist(userSearch,chat_id)

    #Localizamos el ID del chat para realizar el update
    idLocated = findThings(chat_id, method = "Chats", style="_id")
    idLocated = idLocated[-1]

    #¿El usuario ya ha publicado algún mensaje en dicho chat?
    textUser = checkExist(userSearch,chat_id, method="Messages")
    print(textUser)

    #Realizamos la inserción
    print(text)
    if textUser == False:
        db.update({"_id":idLocated}, {"$push":{"messages":{"user_id":userSearch, "message":text}}})
    elif textUser == True:
        text = str(text[0])
        db.update({"_id":idLocated, "messages.user_id":userSearch}, {"$push":{"messages.$.message":text}})
       
    #Devolvemos el ID del chat 
    return dumps(chat_id)


def getMessages(chat_id, param="False"):

    #Seleccionamos database
    db = pickDB(method="Chats")

    #Ejecutamos la query simplificada si procede
    if param == "True":
        filter = {"Position":"0"}
        projection = {"messages.message":1,"_id":0}
        messages1 = db.find(filter=filter,projection=projection)

        messages1 = list(messages1)[0]["messages"]
        totalMessages = [element["message"] for element in messages1]
        totalMessages = [value for element in totalMessages for value in element]

        return json.dumps(totalMessages)

    #Ejecutamos la query general
    filter = {"Position":f"{chat_id}"}
    projection = {"messages":1,"_id":0}
    messages2 = db.find(filter=filter,projection=projection)

    return json.dumps(list(messages2))


def getSentiment(chat_id):

    #Seleccionamos database
    db = pickDB(method="Chats")

