import urllib
from bs4 import BeautifulSoup as soup
import numpy as np
import math


ogPage = input("Enter Round 1 pairings URL (w/ https://):")


page = urllib.request.urlopen(ogPage)
tab = soup(page, "html.parser")
numByes = 0
names = []
html = []
speaks = []
cumeSpeaks = 0
byes = 0
data = tab.find_all(class_= "white smallish padtop padbottom padleft")
dataList = list(data)
length = len(dataList)

for x in range(length):
	if not ("," in str(dataList[x].text.strip())):
		names.append(dataList[x].text.strip())
		html.append(dataList[x].get("href"))
#print (names)




prelimPage  = "https://www.tabroom.com" + str(html[0])
page = urllib.request.urlopen(prelimPage)
tab = soup(page, "html.parser")

data = tab.find_all(class_= "tenth semibold")
dataList = list(data)
length = len(dataList)
totalRounds = []
prelimCounter = 0 

for x in range(length):
	totalRounds.append(dataList[x].text.strip())
for x in (range(len(totalRounds))):
	if ("Round" in totalRounds[x]):
		prelimCounter = prelimCounter + 1
rounds = prelimCounter
times = rounds*2
print(rounds)

totalSpeaks = np.zeros((len(names), times))
highLow = [0]*len(names)
wins = [0]*len(names)

for tms in range(len(html)):
	numByes = 0;	
	ogPage = "https://www.tabroom.com" + str(html[tms])
	page = urllib.request.urlopen(ogPage)
	tab = soup(page, "html.parser")

	data = tab.find_all(class_= "fifth marno")
	dataList = list(data)
	length = len(dataList)

	for x in range(length):
		if (float(dataList[x].text.strip()) > 5):
			totalSpeaks[tms, math.ceil(x/2) - 1] = dataList[x].text.strip()

	data = tab.find_all(class_= "tenth")
	dataList = list(data)
	length = len(dataList)

	for x in range(length):
		if (str(dataList[x].text.strip()) == "Bye"):
			numByes = numByes + 1
			wins[tms] = wins[tms] + 1

	data = tab.find_all(class_= "tenth centeralign semibold")
	dataList = list(data)
	length = len(dataList)
	prelimWL = [0]*length

	for x in range(length):
		if (str(dataList[x].text.strip()) == "W"):
			prelimWL[x] = 1
		if (str(dataList[x].text.strip()) == "L"):
			prelimWL[x] = 0
	if (len(prelimWL) >= rounds):
		for x in range(rounds-numByes):
			if (prelimWL[len(prelimWL)-x-1] == 1):
				wins[tms] = wins[tms] + 1


#print (wins)
#fixing byes
for tms in range(len(names)):
	for rds in range(times):
		cumeSpeaks = cumeSpeaks + totalSpeaks[tms, rds]
		if (totalSpeaks[tms, rds] == 0):
			byes = byes + 1

	avg = cumeSpeaks/(times-byes)
	for rds in range(times):
		if (totalSpeaks[tms, rds] == 0):
			totalSpeaks[tms, rds] = avg
	cumeSpeaks = 0 
	byes = 0

allSpeaks = [0]*len(names)


for x in range(len(allSpeaks)):
	for y in range(times):
		allSpeaks[x] = allSpeaks[x] + totalSpeaks[x,y]


#low high
for tms in range(len(names)):
	max1 = 0
	min1 = 31
	usedMax1 = 0
	usedMin1 = 0
	usedMax2 = 0
	usedMin2 = 0
	max2 = 0
	min2 = 31
	count = 0
	for rds in range(rounds):
		#first speaker
		if (max1 > totalSpeaks[tms, rds*2]):
			max1 = totalSpeaks[tms, rds*2]
		if (min1 < totalSpeaks[tms, rds*2]):
			min1 = totalSpeaks[tms, rds*2]
		#second speaker
		if (max2 > totalSpeaks[tms, rds*2+1]):
			max2 = totalSpeaks[tms, rds*2+1]
		if (min2 < totalSpeaks[tms, rds*2+1]):
			min2 = totalSpeaks[tms, rds*2+1]
	for rds in range(times):
		if (rds%2 == 0 and totalSpeaks[tms, rds] == max1 and usedMax1 == 0):
			usedMax1 = 1
		elif (rds%2 == 0 and totalSpeaks[tms, rds] == min1 and usedMin1 == 0):
			usedMin1 = 1
		elif (rds%2 == 0):
			highLow[tms] = highLow[tms] + totalSpeaks[tms, rds]
			count = count+1

		if (rds%2 == 1 and totalSpeaks[tms, rds] == max1 and usedMax2 == 0):
			usedMax2 = 1
		elif (rds%2 == 1 and totalSpeaks[tms, rds] == min1 and usedMin2 == 0):
			usedMin2 = 1
		elif (rds%2 == 1):
			highLow[tms] = highLow[tms] + totalSpeaks[tms, rds]
			count = count+1
#print (highLow)

prelimWins = []
tempHL = highLow
final = [0]*len(names)
highest = 0;
seeds = []
highestPos = 0;

for totalWins in range(rounds):
	for tms in range(len(names)):
		if (wins[tms] == (rounds-totalWins)):
			prelimWins.append(tms);
	for y in range(len(prelimWins)):
		for x in range(len(prelimWins)):
			if (tempHL[prelimWins[x]] >= highest):
				if (tempHL[prelimWins[x]] == highest):
					if (allSpeaks[prelimWins[x]] > allSpeaks[highestPos]):
						highest = tempHL[prelimWins[x]]
						highestPos = prelimWins[x]
				else: 
					highest = tempHL[prelimWins[x]]
					highestPos = prelimWins[x]
		tempHL[highestPos] = 0
		seeds.append(names[highestPos])
		highest = 0;
		highestPos = 0
	prelimWins = []
for x in range(len(seeds)):
	print(str(x+1) + ". " + str(seeds[x]))







	

#finding actual cume speaks 








