from Src.idGenerator import *
from Src.finding import *
from Src.mongoThings import *
from Src.errorHandler import *
from Src.translator import *

from bson.objectid import ObjectId
import json
import pandas as pd
import numpy as np

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity as distance

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

    #Realizamos la inserción
    if textUser == False:
        db.update({"_id":idLocated}, {"$push":{"messages":{"user_id":userSearch, "message":text}}})
    elif textUser == True:
        text = str(text[0])
        db.update({"_id":idLocated, "messages.user_id":userSearch}, {"$push":{"messages.$.message":text}})
       
    #Devolvemos el ID del chat 
    return dumps(chat_id)


def getMessages(chat_id, simple="False", param="cadena"):

    #Seleccionamos database
    db = pickDB(method="Chats")

    #Ejecutamos la query simplificada si procede
    if simple == "True":
        filter = {"Position":f"{chat_id}"}
        projection = {"messages.message":1,"_id":0}
        messages1 = db.find(filter=filter,projection=projection)

        messages1 = list(messages1)[0]["messages"]
        totalMessages = [element["message"] for element in messages1]
        totalMessages = [value for element in totalMessages for value in element]

        if param == "cadena":
            return json.dumps({"Messages":list(totalMessages)})
        if param == "lista":
            return list(totalMessages)

    #Ejecutamos la query general
    filter = {"Position":f"{chat_id}"}
    projection = {"messages":1,"_id":0}
    messages2 = db.find(filter=filter,projection=projection)

    if param == "cadena":
        return json.dumps(list(messages2)[0])
    if param == "lista":
        return list(messages2) 


def getSentiments(chat_id, alter="False"):

    #Seleccionamos database
    db = pickDB(method="Chats")

    #Tokenización y selección de palabras útiles
    allMessages = getMessages(chat_id, simple="True", param="lista")
    textTokens = tokenize(allMessages)

    #Traducción de mensajes
    translated = transText(allMessages)
 
    #Si la traducción falla, los resultados serán menos precisos
    if translated == False: 
        textWork = textTokens
        if alter == "True":
            analysis = sentimentAnalysis(textWork)
            return json.dumps(analysis)
        analysis = objectiveAnalysis(textWork)
        return json.dumps(analysis)

    elif translated != False:
        textWork = translated
        if alter == "True":
            analysis = objectiveAnalysis(textWork)
            return json.dumps(analysis)
        analysis = sentimentAnalysis(textWork)
        return json.dumps(analysis)


def recomendator(user_id):

    #Seleccionamos database
    dbC = pickDB(method="Chats")
    dbU = pickDB()

    #Obtención de todos los mensajes de un usuario determinado
    # mainUser = findMessages(user_id)

    #Obtención de todos los usuarios que han participado en chats menos el principal

    allUsers = dbU.distinct("Position")
    allUsers = sorted(allUsers)

    #Extracción de mensajes de todos los usuarios menos el principal
    result = [findMessages(element) for element in allUsers]

    result2 = []
    for element in result:
        if element != None:
            result2.append(element)

    #Fusión de values
    newDict = {}

    for element in result2:
        for key, value in element.items():
            test = value
            test2 = " ".join(test)
            newDict[key] = test2
    
    docs = newDict

    count_vectorizer = CountVectorizer()
    sparse_matrix = count_vectorizer.fit_transform(docs.values())
    m = sparse_matrix.todense()

    doc_term_matrix = sparse_matrix.todense()
    df = pd.DataFrame(doc_term_matrix, 
                  columns=count_vectorizer.get_feature_names(), 
                  index=docs.keys())

    similarity_matrix = distance(df,df)

    sim_df = pd.DataFrame(similarity_matrix, columns=docs.keys(), index=docs.keys())

    np.fill_diagonal(sim_df.values, 0)
    try:
        firstUser = sim_df.idxmax()[1]
        secondUser = sim_df.idxmax()[2]
        thirdUser = sim_df.idxmax()[3]
    except IndexError:
        return json.dumps("No hay suficientes usuarios para recomendar")

    total = {user_id: [firstUser, secondUser,thirdUser]}

    return json.dumps(total)