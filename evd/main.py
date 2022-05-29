import pandas as pd
from sklearn import linear_model
from sklearn.preprocessing import PolynomialFeatures
import numpy as np
import csv


def getHexFromCsv():
    result = dict()

    df_companies = pd.read_csv("resources/osm_amenity.csv").fillna('0')
    for i in range(len(df_companies)):
        val = df_companies['geo_h3_10'][i] + ',' + df_companies['city'][i]
        count = [0] * 34
        for j in range(2, len(df_companies.keys()) - 2):
            count[j - 2] = int(df_companies[df_companies.keys()[j]][i])
        result[val] = count

    df_population = pd.read_csv("resources/rosstat_population_all_cities.csv").fillna('0')
    for i in range(len(df_population)):
        val = df_population['geo_h3_10'][i] + ',' + df_population['city'][i]
        if val not in result.keys():
            continue
        result[val][22] = int(df_population['population'][i])

    df_stops = pd.read_csv("resources/osm_stops.csv").fillna('')
    for i in range(len(df_stops)):
        val = df_stops['geo_h3_10'][i] + ',' + df_stops['city'][i]
        if val not in result.keys():
            continue
        match (df_stops['type'][i]):
            case "bus_stop":
                result[val][23] += 1
            case "subway_entrance":
                result[val][24] += 1
            case "tram_stop":
                result[val][25] += 1

    df_roads = pd.read_csv("resources/hexroads.csv").fillna('')
    for i in range(len(df_roads)):
        val = df_roads['geo_h3_10'][i] + ',' + df_roads['city'][i]
        if val not in result.keys():
            continue

        for ind in range(26, 34):
            result[val][ind] = int(df_roads[df_roads.keys()[ind - 23]][i])

    file = open("resources/parsedData/allData.csv", "w")
    for value in result.values():
        string = ""
        for elem in value[:-1]:
            string += str(elem) + ","
        string += str(value[-1]) + "\n"
        file.write(string)
    file.close()

    df_targets = pd.read_csv("resources/target_hakaton_spb.csv").fillna('')
    file = open("resources/parsedData/data2.csv", "w")
    for i in range(len(df_targets)):
        val = df_targets['geo_h3_10'][i] + ',' + df_targets['gorod'][i]
        if val not in result.keys():
            continue

        string = ""
        for elem in result[val]:
            string += str(elem) + ","
        string += str(df_targets['target'][i]) + "\n"
        file.write(string)
    file.close()

    file = open("resources/parsedData/data.csv", "w")
    file.write("Auto parts for foreign cars,Auto repair and maintenance (SRT),"
               "Alcoholic drinks,Pharmacy,Banks,Fast food,Delivery of ready meals,"
               "Womens clothing,Cafe,Cosmetics / Perfume,Nail studios,Vegetables / "
               "Fruits,Hairdressers,Payment terminals,Postamats,Grocery stores,"
               "Points for issuing online orders,Restaurants,Insurance, Supermarkets,"
               "Flowers,Tire Service,population,bus_stop,subway_entrance,tram_stops,"
               "primary,primary_link,secondary,secondary_link,tertiary,residential,"
               "motorway,unclassified,target\n")
    for i in range(len(df_targets)):
        val = df_targets['geo_h3_10'][i] + ',' + df_targets['gorod'][i]
        if val not in result.keys():
            continue

        string = ""
        for elem in result[val]:
            string += str(elem) + ","
        string += str(df_targets['target'][i]) + "\n"
        file.write(string)
    file.close()


def ByCity(city, array, limit):
    i = 0
    while (i < len(array)):
        if (array[i] < limit and array[i] > 0):
            i += 1
        else:
            array.pop(i)

    savearray = array.copy()

    for k in range(len(array)):
        for j in range(6):
            if (neighbors[k][j] >= 0 and neighbors[k][j] < len(savearray)):
                array[k] += (0.1 * savearray[neighbors[k][j]])
    OTVET = []

    for k in range(len(array)):
        if (coords[k][0] == city):
            OTVET.append([coords[k][1], coords[k][2], array[k],
                          PropertyTypeDict[PrivatePropertyForHex[k].index(max(PrivatePropertyForHex[k]))]])
    OTVET.sort(key=lambda x: x[2], reverse=True)
    return OTVET


getHexFromCsv()

PropertyTypeDict = {0: 4, 1: 2, 2: 2, 3: 2, 4: 1, 5: 1, 6: 1, 7: 1, 8: 1,
                    9: 1, 10: 3, 11: 4, 12: 4, 13: 4, 14: 1, 15: 3, 16: 4,
                    17: 1, 18: 3, 19: 1, 20: 4, 21: 2}

coords = []
PrivatePropertyForHex = []
with open('resources/osm_amenity_edited.csv', newline='') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        coords.append([row[1], row[-2], row[-1]])
        PPFH = [0] * 22
        for i in range(2, 22):
            if (row[i] != ''):
                PPFH[i] += int(row[i][:-2])
        PrivatePropertyForHex.append(PPFH)

target = []
with open('resources/parsedData/data.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        target.append(float(row["target"]))

vars = []
with open('resources/parsedData/data2.csv', newline='') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        vars.append(list(map(int, row[:-1])))

all_x = []
with open('resources/parsedData/allData.csv', newline='') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        all_x.append(list(map(int, row)))

neighbors = []
with open('resources/neighborsFINAL.csv', newline='') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        neighbors.append(list(map(int, row[2].split(" ")[:-1])))

vars = np.array(vars)
valuales = np.array(target)
polynom = PolynomialFeatures(degree=2)
x_poly = polynom.fit_transform(vars)
polynom.fit(x_poly, valuales)
lin2 = linear_model.LinearRegression()
lin2.fit(x_poly, valuales)
spbList = ByCity("SPB", list(lin2.predict(polynom.fit_transform(all_x))), 300000)
nnList = ByCity("NN", list(lin2.predict(polynom.fit_transform(all_x))), 50000)
ekbList = ByCity("EKB", list(lin2.predict(polynom.fit_transform(all_x))), 50000)
nskList = ByCity("NSK", list(lin2.predict(polynom.fit_transform(all_x))), 50000)

fileObject = open("resultWoEjection", "w")
fileObject.write("")
fileObject.close()
fileObject = open("resultWoEjection", "a")
fileObject.write("SPB\n");
for spb in spbList:
    fileObject.write(spb[0] + ", " + spb[1] + ", " + str(spb[2]) + ", " + str(spb[3]) + "\n")
fileObject.write("\nNN\n");
for nn in nnList:
    fileObject.write(nn[0] + ", " + nn[1] + ", " + str(nn[2]) + ", " + str(nn[3]) + "\n")

fileObject.write("\nEKB\n");
for ekb in ekbList:
    fileObject.write(ekb[0] + ", " + ekb[1] + ", " + str(ekb[2]) + ", " + str(ekb[3]) + "\n")

fileObject.write("\nNSK\n");
for nsk in nskList:
    fileObject.write(nsk[0] + ", " + nsk[1] + ", " + str(nsk[2]) + ", " + str(nsk[3]) + "\n")
fileObject.close()

spbList = ByCity("SPB", list(lin2.predict(polynom.fit_transform(all_x))), 1000000000)
nnList = ByCity("NN", list(lin2.predict(polynom.fit_transform(all_x))), 1000000000)
ekbList = ByCity("EKB", list(lin2.predict(polynom.fit_transform(all_x))), 1000000000)
nskList = ByCity("NSK", list(lin2.predict(polynom.fit_transform(all_x))), 1000000000)
fileObject = open("resultWithEjection", "w")
fileObject.write("")
fileObject.close()
fileObject = open("resultWithEjection", "a")
fileObject.write("SPB\n");
for spb in spbList:
    fileObject.write(spb[0] + ", " + spb[1] + ", " + str(spb[2]) + ", " + str(spb[3]) + "\n")
fileObject.write("\nNN\n");
for nn in nnList:
    fileObject.write(nn[0] + ", " + nn[1] + ", " + str(nn[2]) + ", " + str(nn[3]) + "\n")

fileObject.write("\nEKB\n");
for ekb in ekbList:
    fileObject.write(ekb[0] + ", " + ekb[1] + ", " + str(ekb[2]) + ", " + str(ekb[3]) + "\n")

fileObject.write("\nNSK\n");
for nsk in nskList:
    fileObject.write(nsk[0] + ", " + nsk[1] + ", " + str(nsk[2]) + ", " + str(nsk[3]) + "\n")
fileObject.close()
