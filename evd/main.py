from sklearn import linear_model
from sklearn.preprocessing import PolynomialFeatures
import numpy as np
import csv

PropertyTypeDict = {0: 1, 1: 2, 2: 4, 3: 1, 4: 2, 5: 1, 6: 2, 7: 1, 8: 1, 9: 1, 10: 4, 11: 4, 12: 4, 13: 2, 14: 2, 15: 1, 16: 2,
       17: 1, 18: 3, 19: 1, 20: 4, 21: 2}

def ByCity(city, array, limit):
    i = 0
    while (i < len(array)):
        if (array[i] < limit and array[i] > 0):
            i += 1
        else:
            array.pop(i)

    savearray = array.copy()
    print(city)

    for k in range(len(array)):
        for j in range(6):
            if(neighbors[k][j] >= 0 and neighbors[k][j] < len(savearray)):
                array[k] += (0.1 * savearray[neighbors[k][j]])
    OTVET = []

    for k in range(len(array)):
        if (coords[k][0] == city):
            OTVET.append([coords[k][1], coords[k][2], array[k], PropertyTypeDict[PrivatePropertyForHex[k].index(max(PrivatePropertyForHex[k]))]])
    OTVET.sort(key=lambda x: x[2], reverse=True)
    return OTVET



coords = []
PrivatePropertyForHex = []
with open('osm_amenity_edited.csv', newline='') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        coords.append([row[1],row[-2],row[-1]])
        PPFH = [0] * 22
        for i in range(2,22):
            if(row[i] != ''):
                PPFH[i] += int(row[i][:-2])
        PrivatePropertyForHex.append(PPFH)

Y = []
with open('data.csv', newline='') as csvfile:
     reader = csv.DictReader(csvfile)
     for row in reader:
         Y.append(int(row["target"]))

x = []
with open('data2.csv', newline='') as csvfile:
     reader = csv.reader(csvfile)
     for row in reader:
         x.append(list(map(int, row[:-1])))

X_all = []
with open('Alldata.csv', newline='') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        X_all.append(list(map(int, row)))

neighbors = []
with open('neighborsFINAL.csv', newline='') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        neighbors.append(list(map(int, row[2].split(" ")[:-1])))

x = np.array(x)
y = np.array(Y)
poly = PolynomialFeatures(degree = 2)
X_poly = poly.fit_transform(x)
poly.fit(X_poly, y)
lin2 = linear_model.LinearRegression()
lin2.fit(X_poly, y)
spb1 = ByCity("Санкт-Петербург", list(lin2.predict(poly.fit_transform(X_all))), 5000000)
nizh_nov1 = ByCity("Нижний Новгород", list(lin2.predict(poly.fit_transform(X_all))), 50000)
ekb1 = ByCity("Екатеринбург", list(lin2.predict(poly.fit_transform(X_all))), 50000)
novos1 = ByCity("Новосибирск", list(lin2.predict(poly.fit_transform(X_all))), 50000)
File_object = open("resultWoEjection", "w")
File_object.write("")
File_object.close()
File_object = open("resultWoEjection", "a")
File_object.write("Санкт-Петербург\n");
for spb in spb1:
    File_object.write(spb[0] + ", " + spb[1] + ", " + str(spb[2])  + ", "+ str(spb[3]) + "\n")
File_object.write("\nНижний Новгород\n");
for nizh in nizh_nov1:
    File_object.write(nizh[0] + ", " + nizh[1] + ", " + str(nizh[2]) + ", " + str(nizh[3]) +  "\n")

File_object.write("\nЕкатеринбург\n");
for ekb in ekb1:
    File_object.write(ekb[0] + ", " + ekb[1] + ", " + str(ekb[2]) + ", " + str(ekb[3]) +  "\n")

File_object.write("\nНовосибирск\n");
for novo in novos1:
    File_object.write(novo[0] + ", " + novo[1] + ", " + str(novo[2]) + ", " + str(novo[3]) + "\n")
File_object.close()



spb1 = ByCity("Санкт-Петербург", list(lin2.predict(poly.fit_transform(X_all))), 1000000000)
nizh_nov1 = ByCity("Нижний Новгород", list(lin2.predict(poly.fit_transform(X_all))), 1000000000)
ekb1 = ByCity("Екатеринбург", list(lin2.predict(poly.fit_transform(X_all))), 1000000000)
novos1 = ByCity("Новосибирск", list(lin2.predict(poly.fit_transform(X_all))), 1000000000)
File_object = open("resultWithEjection", "w")
File_object.write("")
File_object.close()
File_object = open("resultWithEjection", "a")
File_object.write("Санкт-Петербург\n");
for spb in spb1:
    File_object.write(spb[0] + ", " + spb[1] + ", " + str(spb[2]) + ", "+ str(spb[3]) + "\n")
File_object.write("\nНижний Новгород\n");
for nizh in nizh_nov1:
    File_object.write(nizh[0] + ", " + nizh[1] + ", " + str(nizh[2]) + ", " + str(nizh[3]) + "\n")

File_object.write("\nЕкатеринбург\n");
for ekb in ekb1:
    File_object.write(ekb[0] + ", " + ekb[1] + ", " + str(ekb[2]) + ", " + str(ekb[3]) + "\n")

File_object.write("\nНовосибирск\n");
for novo in novos1:
    File_object.write(novo[0] + ", " + novo[1] + ", " + str(novo[2]) + ", " + str(novo[3]) + "\n")
File_object.close()
