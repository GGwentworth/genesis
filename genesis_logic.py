#!/usr/bin/env python2.7

import json
import requests
from datetime import datetime
from pprint import pprint
from pymongo import MongoClient
from time import sleep

#Function that returns a list[last, time, market] of the last NUMBER of samples for MARKET where the first element in the list is the latest data point and the last element in the list is the oldest datapoint. All elements in list are unique
def printLastNumbers( market , number):
	myGraphList = []
	cursor = collections.find({"MarketName": market }).sort("TimeStamp", -1)
	for document in cursor:
		myGraphList.append([document['Last'],document['TimeStamp'],document['MarketName']])
		myGraphList = [list(t) for t in set(tuple(element) for element in myGraphList)]
		if (number == len(myGraphList)):
			myGraphList = sorted(myGraphList,key=lambda l:l[1], reverse=True)
			return myGraphList
	return myGraphList
		
#Function that will return a list of the different markets
def getMarkets():
	url = 'https://bittrex.com/api/v1.1/public/getmarketsummaries'
	myMarketList = []
	counter = 1
	response = requests.get(url)
	json_data = json.loads(response.text)
	responseList = json_data["result"]
	howLong =  len(responseList)
	counterI = 0
	while counterI < howLong - 1 :
		counterI = counterI + 1
		if responseList[counterI]["BaseVolume"] > 1000:
			myMarketList.append(responseList[counterI]['MarketName'])
		
	return myMarketList


#Input printLastNumbers list and returns new list with timestamp converted datetime format
def parseTimeStamps(myList):
	for x in myList:
		format = '%Y-%m-%d %H:%M:%S'
		x[1] = str(x[1]).replace("T", " ")
		x[1] = str(x[1]).split(".", 1)[0]
		x[1] = datetime.strptime(x[1], format)

	return myList

#returns list of last price and time in seconds normalized to 0   where 0 is the lastest  time sample available
def normalizeTimeStamps(myList):
	normalizedList = []
	howLong = len(myList)
	counterI = 0
	while counterI < howLong  :
		normalizedList.append([myList[counterI][0], (myList[0][1] - myList[counterI][1]).total_seconds(), myList[0][2]])
		counterI = counterI + 1

	return normalizedList


#Establishing connection to MongoDB database
client = MongoClient(host=['192.168.1.198:27017'])
#client = MongoClient(host=['108.196.157.14:27017'])

db = client['bittrex']

collections = db['marketSummaries']
# Connection Established


#printLastNumbers( "BTC-LSK" , 50)
#pprint(getMarkets())
#print getMarkets()
##########masterList = normalizeTimeStamps(parseTimeStamps(printLastNumbers("BTC-ARK", 600)))
#masterList = parseTimeStamps(printLastNumbers("BTC-INCNT", 250))
#############print str((  masterList[0][0] - masterList[len(masterList)-1][0]  ) / (  masterList[len(masterList)-1][1] ) ) + "_______" + masterList[0][2]
#print (  masterList[0][0] - masterList[len(masterList)-1][0]  ) / (  masterList[len(masterList)-1][1] )
#pprint(masterList)
#for x in masterList:
#	print str(x[0]) + "-----------" + str(x[1])
#print masterList[0][1] - masterList[3][1]

#pprint(printLastNumbers("BTC-OMG", 250))
displayList = []
loopList = range(500)
loopList.pop(0)
loopList.pop(0)
#loopList.pop(0)
#print loopList
#for x in getMarkets():
lenOfSamples = 10
counter = 0
masterList = normalizeTimeStamps(parseTimeStamps(printLastNumbers("BTC-ADX", lenOfSamples)))
	#pprint(masterList)
while counter < lenOfSamples - 1:
	displayList.append([ ((masterList[counter][0] - masterList[counter + 1][0]) /  masterList[counter][0] ) * 100,  (masterList[counter + 1][1] - masterList[counter ][1]),  ((masterList[0][0] - masterList[counter + 1][0]) /  masterList[0][0] ) * 100, masterList[counter + 1][1], masterList[counter][2]])
	counter = counter + 1
	#print str((  masterList[0][0] - masterList[len(masterList)-1][0]  ) / (  masterList[len(masterList)-1][1] ) ) + "_______" + masterList[0][2] + "______________" + str(masterList[len(masterList)-1][1])
	#displayList.append([(  masterList[0][0] - masterList[len(masterList)-1][0]  ) / (  masterList[len(masterList)-1][1] ), masterList[0][2], masterList[0][0] - masterList[len(masterList)-1][0] , masterList[len(masterList)-1][1] , ((masterList[0][0] - masterList[len(masterList)-1][0]) / masterList[0][0]) * 100  ] )
	#displayList.append([ masterList[0][2],  (masterList[len(masterList)-1][1])/60 , ((masterList[0][0] - masterList[len(masterList)-1][0]) / masterList[0][0]) * 100  ] )

#displayList = sorted(displayList,key=lambda l:l[4], reverse=True)
displayList = sorted(displayList,key=lambda l:l[3], reverse=False)
pprint(displayList)
	#pprint(printLastNumbers( x , 100))
	#print "______________________________________________________________________________________________________________________________________________________"
	#print "______________________________________________________________________________________________________________________________________________________"
	#print "______________________________________________________________________________________________________________________________________________________"
