from bson.json_util import dumps
from Src.finding import *
from Src.mongoThings import *

def idGenerator(method="Users"):

    if method == "Users":
        db = pickDB()
    if method == "Chats":
        db = pickDB(method="Chats")
        
    if db.count() == 0:
        return str(0)
    else:
        projection = {'Position':1}
        limit = 1
        sort = sort=list({'_id': -1}.items())
        lastId = db.find(projection=projection,sort=sort,limit=limit)
        calc = lastId[0]
        calc2 = int(calc["Position"])
        return str(calc2 + 1)