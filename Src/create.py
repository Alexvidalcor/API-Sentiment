from Src.idGenerator import *
from Src.finding import *
from Src.mongoThings import *

from bson.objectid import ObjectId

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

    # #Devolvemos el ID del chat 
    return dumps(int(chat_id))

    
def addMessage(chat_id):

    db = pickDB(method="Chats")

    #Generamos nueva UserID
    newUser = createUser(db, "Pepe")

    #Seleccionamos el chat donde realizar la inserción
  
    selectId = [i for i in db["Chats"].find({"_id": ObjectId('5e500efeae1621687a157a91')})][0]

    #Realizamos la inserción

    selectId2 = selectId["_id"]

    db["Chats"].update({"_id":selectId["_id"]}, {"$addToSet":{"idUsers":newUser}})

    #Devolvemos el ID del chat 

    return dumps(selectId2)
