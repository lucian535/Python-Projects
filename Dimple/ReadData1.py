import time
import sys
import pymongo 

# connect to mongo api
username = "chengl26"
password = "YR84fDOqpFoYJI4S" 

myclient = pymongo.MongoClient(f"mongodb+srv://{username}:{password}@3pdemo.87iodyv.mongodb.net/?retryWrites=true&w=majority&appName=3PDemo")

# sleect appropriate database location
mydb = myclient["user_data"]
mycol = mydb["baby_status"]

# checking user
## change user here
user = "Lucian"

print("READING USER DATA FROM SERVER - test 1 (singular data)")
print("==============================")
print("Connectedto Dimple Server")
print(f"reading data for: {user}")
print("")

userData = [p for p in mycol.find({"name" : user})]
userData = userData[0] # get the user
curFreq = userData["freq"]

print(f'Read data for {user}, frequency : {curFreq}')