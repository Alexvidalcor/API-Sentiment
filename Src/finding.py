from Src.mongoThings import *


def findThings(array, method = "Users", style = "Position", secret=[], length=3,create=True):

    #Seleccionar Database
    if method == "Users":
        db = pickDB()
    if method == "Chats":
        db = pickDB(method = "Chats")

    #Seleccionar detalles adicionales
    if style == "_id":
        selectFilter = "Position"
    if style == "Position":
        selectFilter = "Username"

    #Búsqueda del elemento seleccionado
    result = secret
    try:
        filter = {f"{selectFilter}":array[0]}
        projection = {f"{style}":1}
        limit = 1
        sort = list({'_id': -1}.items())
        users = db.find(filter=filter,limit=limit,projection=projection, sort=sort)
        result.append(users[0][f"{style}"])
        array.remove(array[0])
        findThings(array, method= method, style = style,secret=result,length=length)

    #Creación de nuevo usuario si no existiera
    except IndexError:
        try:
            if create == True:
                from Src.create import createUser
                newUser = createUser(array[0])
                result.append(newUser)
                array.remove(array[0])
                findThings(array, method= method, style = style,secret=result,length=length)
            else:
                raise ValueError("Introducción errónea de usuario")
        except IndexError:
            #Error de retorno
            return result

    except AttributeError:
        filter = {f"{selectFilter}":array[0]}
        projection = {f"{style}":1}
        limit = 1
        sort = list({'_id': -1}.items())
        chats = db.find(filter=filter,limit=limit,projection=projection, sort=sort)
        result.append(chats[0][f"{style}"])
        return result

  
    return result[-length:]


def findMessages(user_id):

    #Seleccionamos Database
    db = pickDB(method = "Chats")

    #Realizamos query principal
    filter = {"messages.user_id":f"{user_id}"}
    projection = {"messages.user_id":1,"messages.message":1,"_id":0}
    userMessages = db.find(filter=filter,projection=projection)

    #Filtramos contenidos en base al id proporcionado
    first = list(userMessages)

    messagesDef = []
    try:
        for element in first:
            intro1 = element["messages"]
            intro2 = intro1
            for element2 in intro2:
                if element2["user_id"] == f"{user_id}":
                    messagesDef.append(element2["message"])

        return {user_id:messagesDef[0]}

    except:
        return None

    