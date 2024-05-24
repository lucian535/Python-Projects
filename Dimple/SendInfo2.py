import time
import sys
import pymongo 
import random

username = "chengl26"
password = "YR84fDOqpFoYJI4S" 

myclient = pymongo.MongoClient(f"mongodb+srv://{username}:{password}@3pdemo.87iodyv.mongodb.net/?retryWrites=true&w=majority&appName=3PDemo")

mydb = myclient["user_data"]
mycol = mydb["baby_status"]

print("SENDING USER DATA TO SERVER - test 2 (continuous random data)")
print("==============================")
print("Connectedto Dimple Server")

user = "Lucian"
print("")
print(f"Updating Values for {user}")

# purposely put in values for hunger and sleepiness 
freqList = [random.randint(0, 7000) for _ in range(10)] + [random.randint(1000, 1999) for _ in range(15)] + [random.randint(0, 7000) for _ in range(20)] + [random.randint(2000, 5000) for _ in range(25)]

# time interval between each data send
timeInterval = 1

print("")
print("Frquencies to be used: ")
print(freqList)

print("")
print("Beginning Data Transfer")
print("==============================")
while True:
    for freq in freqList:
        mycol.update_one({"name" : user}, {"$set" : {"freq" : freq}})
        print(f"updated frequency with {freq}")
        time.sleep(timeInterval)


