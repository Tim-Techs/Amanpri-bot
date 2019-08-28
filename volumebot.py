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
# import pandas as pd
from time import strftime


print("Volume Bot Start")

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
    def __init__(self,threadID,name,counter,setting,botVolume,restAPI):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
        self.setting = setting
        self.botVolume = botVolume
        self.restAPI = restAPI
    def run(self):
        print ("Starting " + self.name)
        runbot(self.name, self.counter, 2,self.setting,self.botVolume,self.restAPI) 
        print("Exiting " + self.name)   

def runbot( threadName, counter,delay,setting,botVolume,restAPI):
    print("*******************Run Bot ************************")
    totalVolume = botVolume
    tmparrays = []
    
    timeFrom = setting[2]
    timeTo = setting[3]
    diff = int(calculateTimeDiff(timeFrom, timeTo))
    print("diff: *************", diff)
    tmparrays = getRandomAmounts(totalVolume,diff)
    print(tmparrays)

    for i in range(diff):
        print('============================')
        print(str(tmparrays[i]))
        timestamp = int(time.time()*1000.0)
        print("TimeStamp : " + str(timestamp))
        print("one min bot:" + str(i) )
        newsetting = getUserInfo(setting[8])
        print(newsetting[12])
        if(newsetting[12] == 1):
            oneminBot(tmparrays[i],restAPI,setting[8])
            while True:
                tmptime = int(time.time()*1000.0)
                print("tmpTime : " +str(tmptime))
                if(timestamp + 60 * 1000 < tmptime):                
                    break
                time.sleep(2)
        else:
            time.sleep(2)        
    
    return   

def getUserInfos():
    # print("getDbInfo")
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
def getUserInfo(userId):
    print("getDbInfo")
    try:
        cnx = mysql.connector.connect(**db_config)
        cursor = cnx.cursor()
        query = ("SELECT id,name,email,email_verified_at,password,remember_token,created_at,updated_at,apikey,secret,bot_status,pricebot_status,volumebot_status from users where id = " + str(userId))
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
    print("getBotPlan ------>")
    try:
        cnx = mysql.connector.connect(**db_config)
        cursor = cnx.cursor()
        query = ("SELECT id,start_date,timefrom,timeto,volume,status,created_at,updated_at,userid,runstate from volumebot where id = " + str(planId))
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
        query = ("SELECT id,start_date,timefrom,timeto,volume,status,created_at,updated_at,userid,runstate from volumebot where userid = " + str(userId) + " and `status` = 'waiting'")
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

def getAmount():
    result = restAPI.get_account()
    coins = result['data']['coin_list']
    amounts = []
    btc_amount = 0
    amal_amount = 0
    for coin in coins:
        if(coin['coin'] == "btc"):
            btc_amount = coin['normal']
        if(coin['coin'] == "amal"):
            amal_amount = coin['normal']    
    print("btc amount: " + str(btc_amount))
    print("amal amount: " + str(amal_amount))
    amounts.append(btc_amount)
    amounts.append(amal_amount)
    return amounts

def Rands(start, end, num):
    res = []
    for j in range(num):
        res.append(random.randint(start,end))
    return res

def getRand(start, end):    
    res = random.randint(start,end)
    return res    
def getRandomAmounts(volume, num):
    total_volume = volume
    randoms = Rands(1,9,num)
    t_amount = 0
    t_amountRange = []
    for ran in randoms:
        t_amount += ran
    print(t_amount)
    for ran in randoms:
        t_amountRange.append(round(total_volume *  ran / t_amount,2)) 
    
    return t_amountRange

def oneminBot(volume,restAPI,userId):
    print("One minutes Volume")
    # symbol = 'crobtc'
    step_price = 0.0000000001
    total_volume = volume
    randoms = Rands(1,9,10)
    t_amount = 0
    t_amountRange = []
    for ran in randoms:
        t_amount += ran
    print(t_amount)
    for ran in randoms:
        t_amountRange.append(round(total_volume *  ran / t_amount,2)) 
    

    for i in range(len(randoms)):
        print('===============================')
        
        newsetting = getUserInfo(userId)        
        if(newsetting[10] == 1):
            print(t_amountRange[i])
            prices = getPrices(restAPI)       
            
            bestask = prices[0]
            bestbid = prices[1]
            step_price = prices[2]
            print('Prices : ' + str(bestask) + " " + str(bestbid) + " " + str(step_price))
            sel_ask = bestask - step_price
            if(sel_ask > bestbid):
                print("condition is ok!!!")                
                if(t_amountRange[i] < 1):
                    t_amountRange[i] = 1
                flag = random.randint(0,1)  
                amounts = getAmount()
                coinAmount = float(amounts[1])
                if(t_amountRange[i] > coinAmount):
                    t_amountRange[i] = coinAmount
                if(flag == 1):
                    print('flag == 1')
                    result = restAPI.create_order(symbol, 'limit', 'sell', t_amountRange[i], sel_ask)
                    result = restAPI.create_order(symbol, 'limit', 'buy', t_amountRange[i], sel_ask)
                    # result = restAPI.cancel_order_all(symbol)
                    print("Volume order finished : " + str(t_amountRange[i]) + "  " + str(sel_ask))
                    getAmount()
                    
                elif(flag == 0):
                    print('flag == 0')
                    result = restAPI.create_order(symbol, 'limit', 'buy', t_amountRange[i], sel_ask)
                    result = restAPI.create_order(symbol, 'limit', 'sell', t_amountRange[i], sel_ask)
                    # result = restAPI.cancel_order_all(symbol)
                    print("Volume order finished : " + str(t_amountRange[i]) + "  " + str(sel_ask))
                    getAmount()
        else:
            break            

        time.sleep(2)
    return    

def getPrices(restAPI):
    prices = []
    result = restAPI.get_market_dept(symbol, 'step0')
    asks = result['data']['tick']['asks']
    bids = result['data']['tick']['bids']
    print(asks)
    print(bids)
    bestask = round(asks[0][0],10)
    bestbid = round(bids[0][0],10)
    print("bestask: " + str(bestask))
    print("bestbid: " + str(bestbid))        
    price_range = round(bestask - bestbid,10)
    print("price range : " + str(price_range * pow(10,10)))
    start = 1
    end = int(price_range * pow(10,10))

    print(end)

    num = random.randint(start,end)
    # print(num)
    step_price = round(num * pow(10,-10),10)
    # print(step_price)

    prices.append(bestask)
    prices.append(bestbid)
    prices.append(step_price)

    return prices   
def changeBotplanStatus(botplanId,status):
    try:
        cnx = mysql.connector.connect(**db_config)
        cursor = cnx.cursor()
        query = ("update volumebot SET `status` = '" + status + "' where id = " + str(botplanId))
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
def compareTime(time1, time2):
    print("compareTime")
    timeA = datetime.strptime(str(time1), "%H:%M:%S")
    timeB = datetime.strptime(str(time2), "%H:%M:%S")

    print(timeA)
    print(timeB)
    diffTime = -1
    if(timeA > timeB):
        print("time Passed")
        return -1        
    else:
        print("waiting Time")   
        diffTime = timeB - timeA 
        print(diffTime.seconds / 60)
        difference = diffTime.seconds / 60

        if(difference > 0 and difference < 1):
            print("start bot")
            return 1
    return 0    
def calculateTimeDiff(time1, time2):  
    print("compareTime")
    timeA = datetime.strptime(str(time1), "%H:%M:%S")
    timeB = datetime.strptime(str(time2), "%H:%M:%S")

    print(timeA)
    print(timeB)
    diffTime = -1
    if(timeA > timeB):
        print("time Passed")
        # return 0        
    else:
        # print("waiting Time")   
        diffTime = timeB - timeA 
        # print(diffTime.seconds / 60)
        difference = diffTime.seconds / 60

        
        return difference
    return 0      
def excuteBot(setting,restAPI):
    print("excute Bot")
    print("=====================")
    
    date = strftime("%H:%M:%S")  
    botPlanId = setting[0]
    botVolume = setting[4]
    botDate = setting[1]
    fromTime = setting[2]
    

    flag = compareTime(date,fromTime)

    if(flag ==  1):
        changeBotplanStatus(setting[0], "pending")
        # result = restAPI.get_ticker('xmxbtc')        
        thread1 = botThread(1, "Thread-1",2,setting,botVolume,restAPI)    
        thread1.start()

        print("Exiting Main Thread")
    elif(flag == 0):
        print("Time is not ready yet") 
    elif(flag == -1):
        print("Time Passed") 
        changeBotplanStatus(botPlanId,"passed")
        
    return

if __name__ == '__main__':
    api_key = '61b5c274c690e8f49e5d46773eafdca6'
    secretkey = '8bea618f045089723cdb9eda7a3a0f1f'
    # REST API
    restAPI = restapi.RestAPI(api_key, secretkey)
    symbol = 'amalbtc'    

    print("Main Function Start !!!")

    while True:
        users = getUserInfos()
        
        for user in users:
            print(user[2])
            # users.append(user) 
            userbotStatus = user[10] 
            pricebotStatus = user[11]   
            volumebotStatus = user[12]   
            api_key = user[8]
            secretkey = user[9]
            userid = user[0] 
            
            results = ""
            if(api_key != "" and api_key != None  and secretkey != "" and secretkey != None):
                restAPI = restapi.RestAPI(api_key, secretkey)
                results = restAPI.get_account()
            else:
                time.sleep(2)
                continue
            print("bot status = " + str(userbotStatus))
            today = date.today()
            print("Today's date:", today)
            if(userbotStatus == 1 and volumebotStatus == 1 and results['msg'] == 'suc'):
                plans = getBotPlans(userid)  
                print("Bot Check log")
                if(plans != -1):          
                    for plan in plans:
                        # print(plan)
                        planDay = plan[1]
                        # print(planDay)
                        if(today == planDay):
                            print("Same day") 
                            excuteBot(plan,restAPI)
                        elif(today > planDay):
                            print("Bot plan day is passed")
                            changeBotplanStatus(plan[0],"passed")
                            
                        else:    
                            print("different day") 

        time.sleep(5) 
              