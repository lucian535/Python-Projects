import pymongo 

try:
    # connect to mongo api
    username = "chengl26"
    password = "" 

    myclient = pymongo.MongoClient(f"mongodb+srv://{username}:{password}@3pdemo.87iodyv.mongodb.net/?retryWrites=true&w=majority&appName=3PDemo")

    print("Connection Successful")
except:
    print("Connection Error")