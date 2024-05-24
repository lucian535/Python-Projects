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

sleepFreq = [1000, 2000] # 1k to 2k hz [1000hz, 2000hz)
hungryFreq = [2000, 5000] # between 2k to 5k hz inclusive [2000hz, 5000hz]

pollingInterval = 1 # seconds
timeForNotificaiton = 7 # seconds
counterRequirement = timeForNotificaiton / pollingInterval

counter = 0
subsequentNotificationsCounter = 0

curSeconds = 0

curBabyStatus = None

print("READING USER DATA FROM SERVER - test 2 (continuous data)")
print("==============================")
print("Connectedto Dimple Server")
print(f"reading data for: {user}")

while True:
    curSeconds += 1
    userData = [p for p in mycol.find({"name" : user})]
    userData = userData[0] # get the user
    curFreq = userData["freq"]

    print(f"Second : {curSeconds} -- frequency : {curFreq}")

    if curFreq >= sleepFreq[0] and curFreq < sleepFreq[1]: # frequencies are for sleepiness
        if curBabyStatus != "Sleepy": # reset counter if frequency ranges change
            counter = 0

        curBabyStatus = "Sleepy"
        counter += 1
    elif curFreq >= hungryFreq[0] and curFreq <= hungryFreq[1]: # frequencies are for hungryness
        if curBabyStatus != "Hungry": # reset counter if frequency ranges change
            counter = 0

        curBabyStatus = "Hungry"
        counter += 1
    else: # Frequencies are irrelevant
        curBabyStatus = None
        counter = 0

    if counter >= counterRequirement:
        if curBabyStatus == "Sleepy":
            print("ALERT! YOUR BABY IS SLEEPY!")

        elif curBabyStatus == "Hungry":
            print("ALERT! YOUR BABY IS HUNGRY!")

    time.sleep(pollingInterval) # sleep for 1s between the polling iteration 