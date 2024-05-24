import time
import sys
import pymongo 

username = "chengl26"
password = "YR84fDOqpFoYJI4S" 

myclient = pymongo.MongoClient(f"mongodb+srv://{username}:{password}@3pdemo.87iodyv.mongodb.net/?retryWrites=true&w=majority&appName=3PDemo")

mydb = myclient["user_data"]
mycol = mydb["baby_status"]

print("SENDING USER DATA TO SERVER - test 1 (singular data)")
print("==============================")
print("Connectedto Dimple Server")

user = input("Input a name to edit data: ")
frequency = int(input("Input simulated detected frequency: "))


userList = [p for p in mycol.find({"name" : user})]

if len(userList) == 0: # user does not exist, create user
    my_dict = {"name" : user, "freq" : frequency}
    mycol.insert_one(my_dict)
    print(f"New user created as {user} with frequency: {frequency}")
else:
    mycol.update_one({"name" : user}, {"$set" : {"freq" : frequency}})
    print(f"Updated user {user} with new frequency: {frequency}")

print("done")