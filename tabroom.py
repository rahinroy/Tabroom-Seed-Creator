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

highLow = [0]*len(names)
wins = [0]*len(names)
for tms in range(len(html)):
    numByes = 0;
    ogPage = "https://www.tabroom.com" + str(html[tms])
    page = urllib.request.urlopen(ogPage)
    tab = soup(page, "html.parser")

    #side or bye
    side = tab.find_all(class_= "tenth")
    sideList = list(side)

    #for x in range(len(sideList)):
#         if (str(sideList[x].text.strip()) == "Bye"):
#             numByes = numByes + 1
            #wins[tms] = wins[tms] + 1
    #round number        
    roundInfo = tab.find_all(class_="tenth semibold")
    roundList = list(roundInfo)
    
    #win or lose
    data = tab.find_all(class_= "tenth centeralign semibold")
    dataList = list(data)
    length = len(dataList)
    
    #opp names
    oppList = list(tab.find_all(class_="white padtop padbottom"))
    if (rounds <= length):
        #print (names[tms] + " " + str(rounds-numByes))
        for x in range(rounds):
            #print (names[tms] + " " + dataList[len(dataList) - 1 - x].text.strip())
            if (dataList[len(dataList) - 1 - x].text.strip() == "W"):
                wins[tms] = wins[tms] + 1
            if (dataList[len(dataList) - 1 - x].text.strip() == ""):
                wins[tms] = wins[tms] + 1
                numByes += 1
    
    
    speaksList = list(tab.find_all(class_="fifth marno"))
    tempList = []
    for x in range(len(speaksList)):
        tempList.append(speaksList[x].text.strip())
    speaks.append(tempList)
    sum1 = 0
    sum2 = 0
    if (len(speaks[tms]) < (rounds*2) and len(speaks[tms]) > 0):
        for y in range(len(speaks[tms])):
            if (y % 2 == 0):
                sum1 = sum1 + float(speaks[tms][y])            
            else:
                sum2 = sum2 + float(speaks[tms][y])
        sum1 = float(sum1 /  ( (len(speaks[tms])) / 2))
        sum1 = float(sum2 /  ( (len(speaks[tms])) / 2))
    for y in range(numByes):
        print(names[tms])
        speaks[tms].append(sum1)
        speaks[tms].append(sum2)






speaker1 = []
speaker2 = []
for x in range(len(speaks)):
    tempList1 = []
    tempList2 = []
    for y in range(len(speaks[x])):
        if (y % 2 == 0):
            tempList1.append(speaks[x][y])
        else:
            tempList2.append(speaks[x][y])
    speaker1.append(tempList1)
    speaker2.append(tempList2)
for x in range(len(speaker1)):
    speaker1[x] = [float(i) for i in speaker1[x]] 
    speaker2[x] = [float(i) for i in speaker2[x]]
for x in range(len(speaker1)):
    if (len(speaker1[x]) > 2):
        speaker1[x].remove(max(speaker1[x]))
        speaker1[x].remove(min(speaker1[x]))
        speaker2[x].remove(min(speaker2[x]))
        speaker2[x].remove(max(speaker2[x]))
total1 = []
total2 = []
totalHL = []
for x in range(len(speaker1)):
    total1.append(sum(speaker1[x]))
    total2.append(sum(speaker2[x]))
for x in range(len(speaker1)):
    totalHL.append(total1[x] + total2[x])
# for x in range(len(names)):
#     print(names[x] + " " + str(wins[x]) + " " + str(speaker1[x]) + " " + str(speaker2[x]) + " " + str(totalHL[x]))

fin = []
for x in reversed(range(rounds+1)):
    temp = []
    for tms in range(len(names)):
        if (wins[tms] == x):
            temp.append(tms) 
    
    dio = {}
    for y in range(len(temp)):
        dio[temp[y]] = totalHL[temp[y]]
    ah = sorted(dio, key=dio.get, reverse=True)
    for p in range(len(ah)):
        fin.append(names[ah[p]])
        #print(names[ah[p]])
for x in range(len(fin)):
    print (str(x+1) + ". " + fin[x])

#finding actual cume speaks 

#https://www.tabroom.com/index/tourn/postings/round.mhtml?tourn_id=15530&round_id=526576