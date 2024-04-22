import xmltodict
from bs4 import BeautifulSoup
import requests
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

fin = open('shop.osm', 'r', encoding='utf-8')
text = fin.read()
fin.close()

def calcArea(mass):
    positive = 0.
    negative = 0.

    for i in range (len(mass)):
        if i != (len(mass) -1):
            positive += mass[i][0]*mass[i+1][1]
            if i >= 1:
                negative -= mass[i][0]*mass[i-1][1]
        else:
            positive += mass[i][0]*mass[0][1]
            negative -= mass[i][0]*mass[i-1][1]

    negative -= mass[0][0]*mass[len(mass) - 1][1]

    area = 0.5 * abs(positive + negative) * 10**10

    return area

ref = 'https://www.openstreetmap.org/node/'
test = 'https://stackoverflow.com/questions/24768858/beautifulsoup-responses-with-error'


massPoint = []
massPoints = []
massResult = []
massAcrossResult = []

countSochi = 0
countVolgograd = 0
countShah = 0
countRost = 0

countMain = 3

massive_sochi = np.zeros(countMain + 1)
massive_volgograd = np.zeros(countMain + 1)
massive_shah = np.zeros(countMain + 1)
massive_rost = np.zeros(countMain + 1)

areasSochi = 0
areasVolgograd = 0
areasShah = 0
areasRost = 0
areasAll = 0

maxAreaSochi = 0
maxAreaVolgograd = 0
maxAreaShah = 0
maxAreaRost = 0

listCity = ['Сочи', 'Волгоград', 'Шахты', 'Ростов-на-Дону']

dct = xmltodict.parse(text)

for way in dct['osm']['way']:

    flagAccessFirst = False
    flagAccessSecond = False

    try:
        for item in way['tag']:
            if item['@k'] == 'name':
                name = item['@v']
            if item['@k'] == 'addr:city':

                if countSochi <= countMain and item['@v'] == 'Сочи':
                    city = item['@v']
                    if item['@v'] in listCity:
                        flagAccessFirst = True
                if countVolgograd <= countMain and item['@v'] == 'Волгоград':
                    city = item['@v']
                    if item['@v'] in listCity:
                        flagAccessFirst = True
                if countShah <= countMain and item['@v'] == 'Шахты':
                    city = item['@v']
                    if item['@v'] in listCity:
                        flagAccessFirst = True
                if countRost <= countMain and item['@v'] == 'Ростов-на-Дону':
                    city = item['@v']
                    if item['@v'] in listCity:
                        flagAccessFirst = True

            if item['@k'] == 'shop':
                if item['@v'] == 'mall':
                    flagAccessSecond = True
    except:
        continue
             

    if not flagAccessFirst or not flagAccessSecond:
        continue

    if city == "Сочи":
        countSochi += 1
    if city == "Волгоград":
        countVolgograd += 1
    if city == "Шахты":
        countShah += 1
    if city == "Ростов-на-Дону":
        countRost += 1

    print("\n ЗДАНИЕ \n")
    print(name)
    print(city)

    n = 0
    for nd in way['nd']:
        newPoint = ref + nd['@ref']

        response = requests.get(newPoint)
        soup = BeautifulSoup(response.text, 'lxml')

        lat = soup.find(class_="latitude").text
        lon = soup.find(class_="longitude").text

        massPoint.append(float(lat))
        massPoint.append(float(lon))
        
        massPoints.append(massPoint)
        
        massPoint = []

    
    area = calcArea(massPoints)

    print(area)
    areasAll += area

    if city == "Сочи":
        massive_sochi[n] = area
        areasSochi += area
        if maxAreaSochi < area:
            maxAreaSochi = area

    elif city == "Волгоград":
        massive_volgograd[n] = area
        areasVolgograd += area
        if maxAreaVolgograd < area:
            maxAreaVolgograd = area

    elif city == "Шахты":
        massive_shah[n] = area
        areasShah += area
        if maxAreaShah < area:
            maxAreaShah = area

    else:
        massive_rost[n] = area
        areasRost += area
        if maxAreaRost < area:
            maxAreaRost = area

    massPoints = []
    massPoint = []

    massAcrossResult.append(city)
    massAcrossResult.append(name)
    massAcrossResult.append(area)

    massResult.append(massAcrossResult)

    massAcrossResult = []

    print('')
    print(massResult)
    n += 1

#2 - средняя площадь зданий для каждого города
avgAreaSochi = areasSochi / countSochi
avgAreaVolgograd = areasVolgograd / countVolgograd
avgAreaShah = areasShah / countShah
avgAreaRost = areasRost / countRost

index = np.arange(4)
values1 = [avgAreaSochi, avgAreaVolgograd, avgAreaShah, avgAreaRost]
plt.bar(index, values1)
plt.xticks(index,['Сочи','Волгоград','Шахты','Ростов-на-Дону'])
plt.title("\nCредняя площадь зданий\nдля каждого города\n")
plt.show()

#3 - максимальная площадь здания для каждого города
index = np.arange(4)
values1 = [maxAreaSochi, maxAreaVolgograd, maxAreaShah, maxAreaRost]
plt.bar(index, values1)
plt.xticks(index,['Сочи','Волгоград','Шахты','Ростов-на-Дону'])
plt.title("\nМаксимальная площадь здания\nдля каждого города\n")
plt.show()

#1 - процентное соотношение суммы площадей одного города с общей площадью всех зданий всех городов
fig = plt.figure(figsize=(6, 6))
ax = fig.add_subplot()

vals = [areasSochi / areasAll, areasVolgograd / areasAll, areasShah / areasAll, areasRost / areasAll]
labels = ['Сочи', 'Волгоград', 'Шахты', 'Ростов-на-Дону']
plt.title("\nПроцентное соотношение суммы площадей\nодного города с общей площадью\nвсех зданий всех городов\n")
exp = (0, 0.1, 0.2, 0.3)
ax.pie(vals, labels = labels, autopct = '%.2f', explode = exp, shadow = True)
ax.grid()
plt.show()
