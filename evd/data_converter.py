import pandas as pd
import h3



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

    file = open("allData.csv", "w")
    for value in result.values():
        string = ""
        for elem in value[:-1]:
            string += str(elem) + ","
        string += str(value[-1]) + "\n"
        file.write(string)
    file.close()

    

getHexFromCsv()