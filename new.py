import numpy as np
import matplotlib.pyplot as plt
import random
import osmnx as ox
import networkx as nx
import seaborn as sns
from gapminder import gapminder # data set
from graph import *

# --------------------------------------------- ФУНКЦИИ ----------------------------------------------------------------
def isNaN(string):              # для проверки nan, если nan, то возвратит True
    return string != string

def calcArea(mass):    # расчет площади здания
    positive = 0.
    negative = 0.

    for i in range(len(mass)):
        if i != (len(mass) - 1):
            positive += mass[i][0] * mass[i + 1][1]
            if i >= 1:
                negative -= mass[i][0] * mass[i - 1][1]
        else:
            positive += mass[i][0] * mass[0][1]
            negative -= mass[i][0] * mass[i - 1][1]

    negative -= mass[0][0] * mass[len(mass) - 1][1]

    area = abs(positive + negative) * 10 ** 10

    return area
# ----------------------------------------------------------------------------------------------------------------------

# --------------------------------------------- ПЕРЕМЕННЫЕ -------------------------------------------------------------
place_name = ['Волгоград', 'Владимир',  'Норильск', 'Таганрог']

mass_answer_itog = []

mass_INFO_CITY = []

AllBusinessAllCities = 0

nass_area_full = [859400000, 124600000, 23160000, 95000000]  # Волгоград, Владимир, Норильск, Таганрог - площадь города всего
# ----------------------------------------------------------------------------------------------------------------------

# --------------------------------------------- ЦИКЛЫ ------------------------------------------------------------------
for iter in range(len(place_name)):
    mass_result_big_business = []
    mass_result_big_builds = []
    mass_cross = []

    mall = ox.geometries_from_place(place_name[iter], tags={'shop': 'mall'}, buffer_dist=5000)
    office = ox.geometries_from_place(place_name[iter], tags={'office': True}, buffer_dist=5000)
    commercial = ox.geometries_from_place(place_name[iter], tags={'building': 'commercial'}, buffer_dist=5000)
    building = ox.geometries_from_place(place_name[iter], tags={'building': True}, buffer_dist=5000)

    mass_with_type_building = []
    mass_with_type_building.append(mall)
    mass_with_type_building.append(office)
    mass_with_type_building.append(commercial)
    mass_with_type_building.append(building)

    massResult_Business = []
    massResult_Builds = []
    summ_area_business = 0.
    summ_area_builds = 0.
    maxAreaCity = 0

    # news_text_txt = open("info_4_city_text.txt", 'w')

    for i in range(len(mass_with_type_building)):
        if i < 3:
            mass = []
            massPoints = []
            massCoordinate = []      # массив с координатами каждого здания
            massCity = []
            massName = []
            massArea = []
            massAccross = []

            for item in mass_with_type_building[i].name:
                # print(item)
                massName.append(item)

            for item in mass_with_type_building[i].geometry:
                try:
                    main = str(item)
                    main = main.replace("POLYGON ((", "")
                    main = main.replace("))", "")
                    main = main.replace(",", "")
                    main = main.split(' ')
                    main = list(map(float, main))
                except:
                    continue

                count = 0

                while count < len(main):
                    mass.append(main[count])
                    mass.append(main[count + 1])
                    massPoints.append(mass)
                    mass = []
                    count += 2

                area = calcArea(massPoints)

                massArea.append(area)

                massCoordinate.append(massPoints[0])  # добавление точки от здания

                massPoints = []

            for j in range(len(massArea)):
                # if not isNaN(massName[j]):
                massAccross.append(place_name[iter])
                massAccross.append(massName[j])
                massAccross.append(massArea[j])
                massAccross.append(massCoordinate[j])               # внесение точки от здания в реузльтирующий массив-
                massResult_Business.append(massAccross)

                summ_area_business += massArea[j]

                if j == 0:
                    maxAreaCity = massArea[j]
                if maxAreaCity < massArea[j]:
                    maxAreaCity = massArea[j]

                massAccross = []

        else:
            mass = []
            massPoints = []
            massCity = []
            massName = []
            massArea = []
            massAccross = []

            for item in mass_with_type_building[i].name:
                massName.append(item)

            for item in mass_with_type_building[i].geometry:
                try:
                    main = str(item)
                    main = main.replace("POLYGON ((", "")
                    main = main.replace("))", "")
                    main = main.replace(",", "")
                    main = main.split(' ')
                    main = list(map(float, main))
                except:
                    continue

                count = 0

                while count < len(main):
                    mass.append(main[count])
                    mass.append(main[count + 1])
                    massPoints.append(mass)
                    mass = []
                    count += 2

                area = calcArea(massPoints)
                massArea.append(area)

                massPoints = []

            for j in range(len(massArea)):
                # if not isNaN(massName[j]):         # ПРОВЕРКА НА NAN
                massAccross.append(place_name[iter])
                massAccross.append(massName[j])
                massAccross.append(massArea[j])
                massResult_Builds.append(massAccross)
                summ_area_builds += massArea[j]

                massAccross = []
    # ----------------------------------------------------------------------------------------------------------------------

    AllBusinessAllCities += summ_area_business

    mass_cross.append(place_name[iter])            # название города
    mass_cross.append(len(massResult_Business))      # кол-во бизнес-центров
    mass_cross.append(summ_area_business)              # площадь всех бизнес-центров
    mass_cross.append(len(massResult_Builds))           # кол-во всех зданий
    mass_cross.append(summ_area_builds)                        # площадь всех зданий
    mass_cross.append(summ_area_business/summ_area_builds)          # относительная площадь
    mass_cross.append(summ_area_business/len(massResult_Business))   # абсолютная площадь
    mass_cross.append(maxAreaCity)                           # максимальная площадь здания бизнес-центра
    mass_cross.append(massResult_Business)

    mass_INFO_CITY.append(mass_cross)      # занос в итоговый массив всех основных характеристик

    print("\n" + f"\n Город - {place_name[iter]}"+ "\n" + str(massResult_Business))

    print (f"\n Город - {place_name[iter]}")

    print("\n Кол-во всех бизнес-центров: " + str(len(massResult_Business)))   # вывод результирующего массива о бизнесс-центрах
    print(" Площадь бизнес-центров: " + f"{summ_area_business}" + "\n")
    print(" Кол-во всех зданий в городе: " + str(len(massResult_Builds)))     # вывод массива о всех зданиях
    print(" Площадь всех зданий: " + f"{summ_area_builds}")

    print("\n Относительная площадь бизнес-центров: " + f"{summ_area_business/summ_area_builds}")
    print("\n Абсолютная площадь бизнес-центров: " + f"{summ_area_business/len(massResult_Business)}")

    print(f" Максмимальная площадь бизнес-здания  в городе составляет: {maxAreaCity}")


# print()
# print(str(mass_INFO_CITY))
#
#---------------------------------------------------------ГРАФИКИ---------------------------------------------------------
# 1 - относительная площадь зданий для каждого города
index = np.arange(4)
values1 = [mass_INFO_CITY[0][5], mass_INFO_CITY[1][5], mass_INFO_CITY[2][5], mass_INFO_CITY[3][5]]
plt.bar(index, values1)
plt.xticks(index, ['Волгоград', 'Владимир', 'Норильск', 'Таганрог'])
plt.title("\nОтносительная площадь зданий\nдля каждого города\n") # отношение площади бизнес-центров к кол-ву бизнес-центров
plt.show()

# 2 - абсолютная площадь зданий для каждого города
index = np.arange(4)
values1 = [mass_INFO_CITY[0][6], mass_INFO_CITY[1][6], mass_INFO_CITY[2][6], mass_INFO_CITY[3][6]]
plt.bar(index, values1)
plt.xticks(index, ['Волгоград', 'Владимир', 'Норильск', 'Таганрог'])
plt.title("\nАбсолютная площадь зданий\nдля каждого города\n") # отношение площади бизнес-центров к суммарной площади всех зданий
plt.show()

# 3 - максимальная площадь здания для каждого города
index = np.arange(4)
values1 = [mass_INFO_CITY[0][7], mass_INFO_CITY[1][7], mass_INFO_CITY[2][7], mass_INFO_CITY[3][7]]
plt.bar(index, values1)
plt.xticks(index, ['Волгоград', 'Владимир', 'Норильск', 'Таганрог'])
plt.title("\nМаксимальная площадь здания\nдля каждого города\n")
plt.show()

# 4 - доля площадей бизнес-центров города к общей площади всех бизнес-центров представленных городов
fig = plt.figure(figsize=(6, 6))
ax = fig.add_subplot()
vals = [mass_INFO_CITY[0][2] / AllBusinessAllCities, mass_INFO_CITY[1][2] / AllBusinessAllCities, mass_INFO_CITY[2][2] / AllBusinessAllCities, mass_INFO_CITY[3][2] / AllBusinessAllCities]
labels = ['Волгоград', 'Владимир', 'Норильск', 'Таганрог']
plt.title("\nДоля площадей бизнес-центров города\nк общей площади всех бизнес-центров\nпредставленных городов\n")
exp = (0, 0.1, 0.2, 0.3)
ax.pie(vals, labels=labels, autopct='%.2f', explode=exp, shadow=True)
ax.grid()
plt.show()

# for i in range(int(mass_INFO_CITY[0][1])):
#     G = ox.graph_from_point(mass_INFO_CITY[0][8][i][3], dist=1000, network_type='drive', simplify=False)

# for i in range(len(mass_INFO_CITY)):
# print ("\n\n")
# print(str(mass_INFO_CITY[0][8][0]))
# print ("\n\n")

#--------------------------------------------------------- КОНЦЕНТРАЦИЯ-------------------------------------------------
mass_Graph = []
mass_Cord = []
mass_shag = []
mass_area = []

for i in range (mass_INFO_CITY[0][1]):             # КОНЦЕТРАЦИЯ БИЗНЕС-ЦЕНТРОВ В ГОРОДЕ (КЛАССТЕРИЗАЦИЯ, ПО КАРТЕ) - ДИАГРАММА РАССЕИВАНИЯ
    mass_recover = []
    mass_recover.append(mass_INFO_CITY[0][8][i][1])
    mass_recover.append(mass_INFO_CITY[0][8][i][3])
    mass_recover.append(mass_INFO_CITY[0][8][i][2])
    mass_Graph.append(mass_recover)

x = []
y = []
print()
print(mass_Graph)

for i in range (len(mass_Graph)):
    x.append(mass_Graph[i][1][0])
    y.append(mass_Graph[i][1][1])
    mass_area.append(mass_Graph[i][2])

    mass_shag.append(x)
    mass_shag.append(y)
    mass_Cord.append(mass_shag)


plt.scatter(x, y, alpha=0.5)
plt.show()
# --------------------------------------------ГРАФ--------------------------------------------------------------------------
draw_graph()
# --------------------------------------------------------------------------------------------------------------------------