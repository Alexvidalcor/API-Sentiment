import traceback
from Src.mongoThings import *

# def jsonErrorHandler(fn):
#     def wrapper(*args, **kwargs):
#         try:
#             print("Calling fn")
#             return fn(*args, **kwargs)
#         except Exception as e:
#             print(traceback.format_exc())
#             return {
#                 "error": str(e)
#             }, 404
#     return wrapper


def checkExist(array, _id, method="Chats"):

    # Seleccionar Database
    db = pickDB(method="Chats")

    # Ejecución de Query
    if method == "Chats":
        try:
            filter = {"$and": [{"Position": f"{_id}"}, {"idUsers": f"{array}"}]}
            projection = {"Position": 1}
            limit = 1
            sort = list({'_id': -1}.items())
            check = db.find(filter=filter, limit=limit,projection=projection, sort=sort)
            test = check[0]
        except IndexError:
            raise IndexError("Usuario no encontrado en el chat seleccionado")

    if method == "Messages":
        try:
            # filter = {"messages.user_id":f"{array}"}

            filter = {"$and": [{"Position": f"{_id}"}, {"messages.user_id":f"{array}"}]}
            projection = {"Position": 1,"_id":0}
            limit = 1
            sort = list({'_id': -1}.items())
            check = db.find(filter=filter, limit=limit,projection=projection, sort=sort)
            check[0]
            return True
        except IndexError:
            return False
