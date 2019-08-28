import biki.rest_api as restapi

import threading
import requests
import json
import time
from datetime import date
from datetime import datetime
import random
import calendar
import hashlib 
import mysql.connector
from mysql.connector import errorcode

import math 

from time import strftime
import datetime

main_url = 'https://openapi.biki.com'

db_config = {
  'user': 'root',
  'password': '',
  'host': '127.0.0.1',
  'database': 'marketingbot'  
}

user_count = 0
exitFlag = 0
users = []


threads = []
api_key = ''
secretkey = ''

class botThread(threading.Thread):
    def __init__(self,threadID,name,counter,setting,side,bottype):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
        self.setting = setting
        self.side = side
        self.bottype = bottype

    def run(self):
        print ("Starting " + self.name)
        runbot(self.name, self.counter, 2,self.setting,self.side,self.bottype) 
        print("Exiting " + self.name)   

def getUserInfos():
    print("getDbInfo")
    try:
        cnx = mysql.connector.connect(**db_config)
        cursor = cnx.cursor()
        query = ("SELECT id,name,email,email_verified_at,password,remember_token,created_at,updated_at,apikey,secret,bot_status,pricebot_status,volumebot_status from users")
        cursor.execute(query)
        results = cursor.fetchall()
        # print(results)
        cursor.close()       
        return results
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
        else:
                print(err)
        return -1
    else:       
        cnx.close()
        return -1
def getUserInfo(userid):
    print("getDbInfo")
    try:
        cnx = mysql.connector.connect(**db_config)
        cursor = cnx.cursor()
        query = ("SELECT id,name,email,email_verified_at,password,remember_token,created_at,updated_at,apikey,secret,bot_status,pricebot_status,volumebot_status from users where id = " + str(userid))
        cursor.execute(query)
        results = cursor.fetchone()
        # print(results)
        cursor.close()       
        return results
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
        else:
                print(err)
        return -1
    else:       
        cnx.close()
        return -1


def getBotPlan(planId):
    try:
        cnx = mysql.connector.connect(**db_config)
        cursor = cnx.cursor()
        query = ("SELECT id,created_at,updated_at,start_date,timefrom,timeto,side,volume,startprice,status,userid,bottype,percentage,runstate from botplans where id = " + str(planId))
        cursor.execute(query)
        results = cursor.fetchone()
        # print(results)
        cursor.close()       
        return results
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
        else:
                print(err)
        return -1
    else:       
            cnx.close()
            return -1
    return         

def getBotPlans(userId):
    try:
        cnx = mysql.connector.connect(**db_config)
        cursor = cnx.cursor()
        query = ("SELECT id,created_at,updated_at,start_date,timefrom,timeto,side,volume,startprice,status,userid,bottype,percentage,runstate from botplans where userid = " + str(userId) + " and `status` = 'waiting'")
        cursor.execute(query)
        results = cursor.fetchall()
        # print(results)
        cursor.close()       
        return results
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
        else:
                print(err)
        return -1
    else:       
            cnx.close()
            return -1
    return    

def changeBotplanStatus(botplanId,status):
    try:
        cnx = mysql.connector.connect(**db_config)
        cursor = cnx.cursor()
        query = ("update botplans SET `status` = '" + status + "' where id = " + str(botplanId))
        print(query)
        cursor.execute(query)

        cnx.commit()
        
        print("Changed botplan status to " + status)
        cursor.close()       
        return
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
        else:
                print(err)
        return -1
    else:       
            cnx.close()
            return -1
    return 

def runbot( threadName, counter,delay,setting,botSide,botType):
    print("Run Bot")

    if(botType == "oneTime"):
        oneTimeBot(botSide,setting)
    elif(botType == "twoHours"):
        twoHoursBot(botSide,setting)
    elif(botType == "someHours"):
        someHoursBot(botSide,setting)
    elif(botType == "automaticOrder"):
        automaticOrderBot(botSide,setting)
    elif(botType == "random"):
        randomBot(botSide,setting)

def getMindParams():
    min = 10000
    max = 13000

    priceArray = []
    priceArray.append(min)
    
    i = 0 
    while i < 1:
        tmpPrice = random.randint(min, max)
        print(tmpPrice)
        priceArray.append(tmpPrice)
        i += 1

    priceArray.append(max)    

    print(priceArray)
    return

def timeDiff(time1, time2):
    timeA = datetime.datetime.strptime(str(time1), "%H:%M:%S")
    timeB = datetime.datetime.strptime(str(time2), "%H:%M:%S")
    

    print(timeA)
    print(timeB)
    if(timeA > timeB):
        print("time Passed")
        return -1
    else:
        diffTime = timeB - timeA
        print(diffTime.seconds)
        print("*********************")
        return  diffTime.seconds  

def compareTime(time1, time2):
    print("compareTime")
    timeA = datetime.datetime.strptime(str(time1), "%H:%M:%S")
    timeB = datetime.datetime.strptime(str(time2), "%H:%M:%S")

    print(timeA)
    print(timeB)
    diffTime = -1
    if(timeA > timeB):
        print("time Passed")
    else:
        print("waiting Time")   
        diffTime = timeB - timeA 
        print(diffTime.seconds / 60)
        difference = diffTime.seconds / 60

        if(difference > 0 and difference < 1):
            print("start bot")
            return 1

    return 0

def oneTimeBot(side,setting):
    print("Start OneTime Bot")
    result = restAPI.get_ticker(symbol)  

    if(side == 0):
        print("Price Raise bot")
        lastPrice = result['data']['last']
        currentSellPrice = result['data']['sell']
        currentBuyPrice = result['data']['buy']

        tmpMinPrice = currentSellPrice * math.pow(10,10)
        percentage = int(setting[12] + 100)
        print(percentage)
        tmpMaxPrice = int(tmpMinPrice * percentage / 100)
        tmpOrders = []
        tmpVolume = 0

        print(tmpMinPrice)
        print(tmpMaxPrice)   
        results = restAPI.get_market_dept(symbol, 'step0')['data']['tick']['asks']  
        
        for i in range(len(results)):
            # print(results[i])
            if(tmpMaxPrice >= results[i][0] * math.pow(10,10)):
                tmpOrders.append(results[i])
                tmpVolume += results[i][1] * results[i][0]
        if(tmpVolume > 0):
            print("Create Order") 
            print(tmpMinPrice)
            print(tmpMaxPrice)  
            print(tmpVolume)
            volume = round(tmpVolume,10)
            print(volume)
            #############################      
            result = restAPI.create_order(symbol, 'market', 'buy',volume)
            # print(str(result))
    elif(side == 1):
        print("Price Fail bot")   
        lastPrice = result['data']['last']
        currentSellPrice = result['data']['sell']
        currentBuyPrice = result['data']['buy']
        print("&&&&&&&&&&&&&&&&&&&&&&")
        percentage = int(100 - setting[12])
        tmpMaxPrice = currentBuyPrice * math.pow(10,10)
        tmpMinPrice = int(tmpMaxPrice * percentage / 100)
        tmpOrders = []
        tmpVolume = 0

        print(tmpMinPrice)
        print(tmpMaxPrice)   
        results = restAPI.get_market_dept(symbol, 'step0')['data']['tick']['bids']  

        for i in range(len(results)):
            # print(results[i])
            if(tmpMinPrice <= results[i][0] * math.pow(10,10)):
                tmpOrders.append(results[i])
                tmpVolume += results[i][1] * results[i][0]
        print(tmpOrders)   
        

        if(tmpVolume > 0):
            print("Create Order") 
            print(tmpMinPrice)
            print(tmpMaxPrice)  
            print(tmpVolume)
            #############################      
            restAPI.create_order(symbol, 'market', 'sell',round(tmpVolume,10))  

     
    changeBotplanStatus(setting[0], "done")
    return
def twoHoursBot(side,setting):
    print("Start twoHours Bot")
    result = restAPI.get_ticker('xmxbtc')  

    if(side == 0):
        print("Price Raise bot")
        lastPrice = result['data']['last']
        currentSellPrice = result['data']['sell']
        currentBuyPrice = result['data']['buy']

        # print(lastPrice)
        # print(currentSellPrice)
        # print("&&&&&&&&&&&&&&&&&&&&&&")
        # print(currentSellPrice * math.pow(10,10))

        percentage = int(100 + setting[12])

        tmpMinPrice = currentSellPrice * math.pow(10,10)
        tmpMaxPrice = int(tmpMinPrice * percentage / 100)

        print(tmpMinPrice)
        print(tmpMaxPrice)

        fromTime = setting[4]
        toTime = setting[5]

        timeRange = 120
        priceRange = []
        priceRange.append(tmpMinPrice)
        i = 1
        while i < 3:
            print(i)
            tmp = random.randint(int(tmpMinPrice), int(tmpMaxPrice))
            priceRange.append(tmp)
            i += 1
        priceRange.append(tmpMaxPrice)    
        # print(priceRange)    
        # print(priceRange[1])

        timeInterval =  timeRange / 3    
        # print(timeRange)
        timeArray = []
        timeArray.append(0)
        j = 1
        while j < 3:
            timeArray.append(j * timeInterval)
            j += 1
        timeArray.append(timeRange)    
        print("*******************")
        print(timeArray) 
        tmpInterval = 0   
        if(timeRange != -1):
            delay = 5
            counter  =  timeRange /  delay 
            i = 0       
            while i < timeRange:
                if(i > timeArray[tmpInterval]):
                    print("^^^^^^^^^^^^^")
                    newsetting = getUserInfo(setting[10])
                    if(newsetting[11] == 1):
                        # print(restAPI.get_account())
                        print(priceRange[tmpInterval])
                        
                        tmpPrice = priceRange[tmpInterval] / math.pow(10,10)
                        result = restAPI.get_market_dept(symbol, 'step0')
                        print(result['data']['tick']['asks'][0][0])

                        if(tmpPrice >= result['data']['tick']['asks'][0][0]):
                            print("Create Order")
                            volume = result['data']['tick']['asks'][0][0] * result['data']['tick']['asks'][0][1]
                            print("volume: " + str(volume))
                            restAPI.create_order(symbol, 'market', 'buy',round(volume,10))
                            condition = True
                            while condition:
                                print("while loop !!!!")
                                result = restAPI.get_market_dept(symbol, 'step0')
                                if(tmpPrice >= result['data']['tick']['asks'][0][0]):
                                    volume = result['data']['tick']['asks'][0][0] * result['data']['tick']['asks'][0][1]
                                    restAPI.create_order(symbol, 'market', 'buy',round(volume,10))
                                    time.sleep(3)
                                else:
                                    condition = False    
                                time.sleep(3)
                        tmpInterval += 1
                    else:
                        time.sleep(2) 
                        tmpInterval += 1       

                time.sleep(delay)
                print("%s: " % ( time.ctime(time.time())))  
                print(i)
                i += delay 
        
    elif(side == 1):
        print("Price Fail bot")          
        lastPrice = result['data']['last']
        currentSellPrice = result['data']['sell']
        currentBuyPrice = result['data']['buy']

        # print(lastPrice)
        # print(currentSellPrice)
        # print("&&&&&&&&&&&&&&&&&&&&&&")
        # print(currentSellPrice * math.pow(10,10))

        percentage = int(100 - setting[12])

        tmpMaxPrice = currentBuyPrice * math.pow(10,10)
        tmpMinPrice = int(tmpMaxPrice * percentage / 100)

        print(tmpMinPrice)
        print(tmpMaxPrice)

        fromTime = setting[4]
        toTime = setting[5]

        timeRange = 7200
        priceRange = []
        priceRange.append(tmpMaxPrice)
        i = 1
        while i < 3:
            print(i)
            tmp = random.randint(tmpMinPrice, tmpMaxPrice)
            priceRange.append(tmp)
            i += 1
        priceRange.append(tmpMinPrice)    
        print(priceRange)    
        print(priceRange[1])

        timeInterval =  timeRange / 3    
        print(timeRange)
        timeArray = []
        timeArray.append(0)
        j = 1
        while j < 3:
            timeArray.append(j * timeInterval)
            j += 1
        timeArray.append(timeRange)    
        print(timeArray) 
        tmpInterval = 0   
        if(timeRange != -1):
            delay = 5
            counter  =  timeRange /  delay 
            i = 0       
            while i < timeRange:
                if(i > timeArray[tmpInterval]):
                    print("^^^^^^^^^^^^^")
                    newsetting = getUserInfo(setting[10])
                    if(newsetting[11] == 1):
                        # print(restAPI.get_account())
                        print(priceRange[tmpInterval])
                        
                        tmpPrice = priceRange[tmpInterval] / math.pow(10,10)
                        result = restAPI.get_market_dept(symbol, 'step0')
                        print(result['data']['tick']['bids'][0][0])

                        if(tmpPrice <= result['data']['tick']['bids'][0][0]):
                            print("Create Order")
                            volume = result['data']['tick']['bids'][0][0] * result['data']['tick']['bids'][0][1]
                            print("volume: " + str(volume))
                            restAPI.create_order(symbol, 'market', 'sell', round(volume,10))
                            print("^^^^^^^^^^^^^^^^^&&&^^^^^^^^^^^^^^^^^^^^^")
                            condition = True
                            while condition:
                                print("while loop !!!!")
                                result = restAPI.get_market_dept('xmxbtc', 'step0')
                                if(tmpPrice <= result['data']['tick']['bids'][0][0]):
                                    volume = result['data']['tick']['bids'][0][0] * result['data']['tick']['bids'][0][1]
                                    restAPI.create_order(symbol, 'market', 'sell', round(volume,10))
                                    print("^^^^^^^^^^^^^^^^^^&&&^^^^^^^^^^^^^^^^^^^^")
                                    time.sleep(3)
                                else:
                                    condition = False    
                                time.sleep(3)
                        tmpInterval += 1
                    else:
                        time.sleep(2)   
                        tmpInterval += 1     

                time.sleep(delay)
                print("%s: " % ( time.ctime(time.time())))  
                print(i)
                i += delay    

     
    changeBotplanStatus(setting[0], "done")
    return
def someHoursBot(side,setting):
    print("Start Random Bot")
    result = restAPI.get_ticker('xmxbtc')  

    if(side == 0):
        print("Price Raise bot")
        lastPrice = result['data']['last']
        currentSellPrice = result['data']['sell']
        currentBuyPrice = result['data']['buy']

        # print(lastPrice)
        # print(currentSellPrice)
        # print("&&&&&&&&&&&&&&&&&&&&&&")
        # print(currentSellPrice * math.pow(10,10))
        percentage = int(100 + setting[12])

        tmpMinPrice = currentSellPrice * math.pow(10,10)
        tmpMaxPrice = int(tmpMinPrice * percentage / 100)

        print(tmpMinPrice)
        print(tmpMaxPrice)

        fromTime = setting[4]
        toTime = setting[5]

        timeRange = timeDiff(fromTime, toTime)
        priceRange = []
        priceRange.append(tmpMinPrice)
        i = 1
        while i < 3:
            print(i)
            tmp = random.randint(tmpMinPrice, tmpMaxPrice)
            priceRange.append(tmp)
            i += 1
        priceRange.append(tmpMaxPrice)    
        # print(priceRange)    
        # print(priceRange[1])

        timeInterval =  timeRange / 3    
        print(timeRange)
        timeArray = []
        j = 1

        while j < 3:
            timeArray.append(j * timeInterval)
            j += 1
        timeArray.append(timeRange)    
        print(timeArray) 
        tmpInterval = 0   
        if(timeRange != -1):
            delay = 5
            counter  =  timeRange /  delay 
            i = 0       
            while i < timeRange:
                if(i > timeArray[tmpInterval]):
                    print("^^^^^^^^^^^^^")
                    newsetting = getUserInfo(setting[10])
                    if(newsetting[11] == 1):
                        # print(restAPI.get_account())
                        print(priceRange[tmpInterval])
                        
                        tmpPrice = priceRange[tmpInterval] / math.pow(10,10)
                        result = restAPI.get_market_dept(symbol, 'step0')
                        print(result['data']['tick']['asks'][0][0])

                        if(tmpPrice >= result['data']['tick']['asks'][0][0]):
                            print("Create Order")
                            volume = result['data']['tick']['asks'][0][0] * result['data']['tick']['asks'][0][1]
                            print("volume: " + str(volume))
                            restAPI.create_order(symbol, 'market', 'buy', round(volume,10))
                            condition = True
                            while condition:
                                print("while loop !!!!")
                                result = restAPI.get_market_dept(symbol, 'step0')
                                if(tmpPrice >= result['data']['tick']['asks'][0][0]):
                                    volume = result['data']['tick']['asks'][0][0] * result['data']['tick']['asks'][0][1]
                                    restAPI.create_order(symbol, 'market', 'buy', round(volume,10))
                                    time.sleep(3)
                                else:
                                    condition = False    
                                time.sleep(3)
                        tmpInterval += 1
                    else:
                        time.sleep(2)  
                        tmpInterval += 1  

                time.sleep(delay)
                print("%s: " % ( time.ctime(time.time())))  
                print(i)
                i += delay 
        
    elif(side == 1):
        print("Price Fail bot")         
        lastPrice = result['data']['last']
        currentSellPrice = result['data']['sell']
        currentBuyPrice = result['data']['buy']

        # print(lastPrice)
        # print(currentSellPrice)
        # print("&&&&&&&&&&&&&&&&&&&&&&")
        # print(currentSellPrice * math.pow(10,10))

        percentage = int(100 - setting[12])

        tmpMaxPrice = currentBuyPrice * math.pow(10,10)
        tmpMinPrice = int(tmpMaxPrice * percentage / 100)

        print(tmpMinPrice)
        print(tmpMaxPrice)

        fromTime = setting[4]
        toTime = setting[5]

        timeRange = timeDiff(fromTime, toTime)
        priceRange = []
        priceRange.append(tmpMaxPrice)
        i = 1
        while i < 3:
            print(i)
            tmp = random.randint(tmpMinPrice, tmpMaxPrice)
            priceRange.append(tmp)
            i += 1
        priceRange.append(tmpMinPrice)    
        # print(priceRange)    
        # print(priceRange[1])

        timeInterval =  timeRange / 3    
        print(timeRange)
        timeArray = []
        timeArray.append(0)
        j = 1
        while j < 3:
            timeArray.append(j * timeInterval)
            j += 1
        timeArray.append(timeRange)    
        print(timeArray) 
        tmpInterval = 0   
        if(timeRange != -1):
            delay = 5
            counter  =  timeRange /  delay 
            i = 0       
            while i < timeRange:
                if(i > timeArray[tmpInterval]):
                    print("^^^^^^^^^^^^^")
                    newsetting = getUserInfo(setting[10])
                    if(newsetting[11] == 1):
                        # print(restAPI.get_account())
                        print(priceRange[tmpInterval])
                        
                        tmpPrice = priceRange[tmpInterval] / math.pow(10,10)
                        result = restAPI.get_market_dept(symbol, 'step0')
                        print(result['data']['tick']['bids'][0][0])

                        if(tmpPrice <= result['data']['tick']['bids'][0][0]):
                            print("Create Order")
                            volume = result['data']['tick']['bids'][0][0] * result['data']['tick']['bids'][0][1]
                            print("volume: " + str(volume))
                            restAPI.create_order(symbol, 'market', 'sell', round(volume,10))
                            condition = True
                            while condition:
                                print("while loop !!!!")
                                result = restAPI.get_market_dept(symbol, 'step0')
                                if(tmpPrice <= result['data']['tick']['bids'][0][0]):
                                    volume = result['data']['tick']['bids'][0][0] * result['data']['tick']['bids'][0][1]
                                    restAPI.create_order(symbol, 'market', 'sell', round(volume,10))
                                    time.sleep(3)
                                else:
                                    condition = False    
                                time.sleep(3)
                        tmpInterval += 1
                    else:
                        time.sleep(2)
                        tmpInterval += 1        

                time.sleep(delay)
                print("%s: " % ( time.ctime(time.time())))  
                print(i)
                i += delay      

     
    changeBotplanStatus(setting[0], "done")
    return

       
def randomBot(side,setting):
    print("Start Random Bot")
    result = restAPI.get_ticker('xmxbtc')  

    if(side == 0):
        print("Price Raise bot")
        lastPrice = result['data']['last']
        currentSellPrice = result['data']['sell']
        currentBuyPrice = result['data']['buy']

        # print(lastPrice)
        # print(currentSellPrice)
        # print("&&&&&&&&&&&&&&&&&&&&&&")
        # print(currentSellPrice * math.pow(10,10))

        tmpMinPrice = currentSellPrice * math.pow(10,10)
        tmpMaxPrice = int(tmpMinPrice * 115 / 100)

        # print(tmpMinPrice)
        # print(tmpMaxPrice)

        fromTime = setting[4]
        toTime = setting[5]

        timeRange = timeDiff(fromTime, toTime)
        priceRange = []
        priceRange.append(tmpMinPrice)
        i = 1
        while i < 3:
            print(i)
            tmp = random.randint(tmpMinPrice, tmpMaxPrice)
            priceRange.append(tmp)
            i += 1
        priceRange.append(tmpMaxPrice)    
        # print(priceRange)    
        # print(priceRange[1])

        timeInterval =  timeRange / 3    
        print(timeRange)
        timeArray = []
        j = 1

        while j < 3:
            timeArray.append(j * timeInterval)
            j += 1
        timeArray.append(timeRange)    
        print(timeArray) 
        tmpInterval = 0   
        if(timeRange != -1):
            delay = 5
            counter  =  timeRange /  delay 
            i = 0       
            while i < timeRange:
                if(i > timeArray[tmpInterval]):
                    print("^^^^^^^^^^^^^")
                    # print(restAPI.get_account())
                    print(priceRange[tmpInterval])
                    
                    tmpPrice = priceRange[tmpInterval] / math.pow(10,10)
                    result = restAPI.get_market_dept('xmxbtc', 'step0')
                    print(result['data']['tick']['asks'][0][0])

                    if(tmpPrice >= result['data']['tick']['asks'][0][0]):
                        print("Create Order")
                        volume = result['data']['tick']['asks'][0][0] * result['data']['tick']['asks'][0][1]
                        print("volume: " + str(volume))
                        restAPI.create_order('xmxbtc', 'market', 'buy', round(volume,10))
                        condition = True
                        while condition:
                            print("while loop !!!!")
                            result = restAPI.get_market_dept('xmxbtc', 'step0')
                            if(tmpPrice >= result['data']['tick']['asks'][0][0]):
                                volume = result['data']['tick']['asks'][0][0] * result['data']['tick']['asks'][0][1]
                                restAPI.create_order('xmxbtc', 'market', 'buy', round(volume,10))
                                time.sleep(3)
                            else:
                                condition = False    
                            time.sleep(3)
                    tmpInterval += 1

                time.sleep(delay)
                print("%s: " % ( time.ctime(time.time())))  
                print(i)
                i += delay 
        
    elif(side == 1):
        print("Price Fail bot")      

     
    changeBotplanStatus(setting[0], "done")
    return    
def automaticOrderBot(side,setting):
    return
def excuteBot(setting):
    print("excute Bot")
    print("=====================")
    
    date = strftime("%H:%M:%S")
    print(date)  

    botPlanId = setting[0] 
    
    botSide = setting[6]
    botVolume = setting[7]
    botPrice = setting[8]
    botDate = setting[3]
    fromTime = setting[4]
    toTime = setting[5]
    botType = setting[11]
    flag = compareTime(date,fromTime)
    if(flag ==  1):
        changeBotplanStatus(setting[0], "pending")
        result = restAPI.get_ticker('xmxbtc')        
        thread1 = botThread(1, "Thread-1",2,setting,botSide,botType)    
        thread1.start()

        print("Exiting Main Thread")
    else:
        changeBotplanStatus(setting[0], "passed")
        print("Time is not ready yet")
        
    return


if __name__ == '__main__':

    api_key = '61b5c274c690e8f49e5d46773eafdca6'
    secretkey = '8bea618f045089723cdb9eda7a3a0f1f'

    # REST API
    restAPI = restapi.RestAPI(api_key, secretkey)

    symbol = 'amalbtc'
    
    print("Main Function Start !!!")
    while True:
        results = getUserInfos()
        user_count = len(results)
        print("User count = " + str(user_count))

        for result in results:
            users.append(result) 
            userbotStatus = result[10]  
            pricebotStatus = result[11]   
            volumebotStatus = result[12]      

            api_key = result[8]
            secretkey = result[9]
            print("bot status = " + str(userbotStatus))

            if(api_key != "" and api_key != None  and secretkey != "" and secretkey != None):
                restAPI = restapi.RestAPI(api_key, secretkey)
                results = restAPI.get_account()
            else:
                time.sleep(2)
                continue

            today = date.today()
            print("Today's date:", today)
            uId = result[0]
            if(userbotStatus == 1 and pricebotStatus == 1):
                plans = getBotPlans(uId)
                
                for plan in plans:
                    planDay = plan[3]
                    print(planDay)
                    if(today == planDay):
                        print("Same day") 
                        
                        excuteBot(plan)
                    elif(today > planDay):
                        print("Bot plan day is passed")
                        changeBotplanStatus(plan[0],"passed")
                    else:    
                        print("different day")   
        time.sleep(5)   
        
    
        


