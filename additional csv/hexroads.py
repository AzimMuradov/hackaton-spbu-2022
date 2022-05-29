import pandas as pd
import h3

df_roads = pd.read_csv("roads_dataset.csv")
df_roads = df_roads.fillna('')
df_population = pd.read_csv("rosstat_population_all_cities.csv")
df_population = df_population.fillna('')

# road counters on hex
df_hexroads = pd.DataFrame(data=df_population['geo_h3_10'])
df_hexroads['city'] = df_population['city']
primary = [0] * df_population.shape[0]
primary_link = [0] * df_population.shape[0]
secondary = [0] * df_population.shape[0]
secondary_link = [0] * df_population.shape[0]
tertiary = [0] * df_population.shape[0]
residential = [0] * df_population.shape[0]
motorway = [0] * df_population.shape[0]
unclassified = [0] * df_population.shape[0]

df_hexroads['primary'] = primary
df_hexroads['primary_link'] = primary_link
df_hexroads['secondary'] = secondary
df_hexroads['secondary_link'] = secondary_link
df_hexroads['tertiary'] = tertiary
df_hexroads['residential'] = residential
df_hexroads['motorway'] = motorway
df_hexroads['unclassified'] = unclassified

for i in range(df_roads.shape[0]):
    roads = df_roads['geometry'][i][12:len(df_roads['geometry'][i])-1]
    roads = roads.split(', ')
    currentCity = df_roads['city'][i]
    for road in roads:
        road = road.split()
        h3hex1 = h3.geo_to_h3(float(road[0]), float(road[1]), 10) 
        h3hex2 = h3.geo_to_h3(float(road[1]), float(road[0]), 10) # там новосибирск сломан был
        req = df_hexroads['geo_h3_10'].isin([h3hex1, h3hex2])
        if (df_roads['highway'][i] == 'primary'):
            df_hexroads.loc[df_hexroads['geo_h3_10'].isin([h3hex1, h3hex2]), 'primary'] += 1
        if (df_roads['highway'][i] == 'primary_link'):
            df_hexroads.loc[df_hexroads['geo_h3_10'].isin([h3hex1, h3hex2]), 'primary_link'] += 1
        if (df_roads['highway'][i] == 'secondary'):
            df_hexroads.loc[df_hexroads['geo_h3_10'].isin([h3hex1, h3hex2]), 'secondary'] += 1
        if (df_roads['highway'][i] == 'secondary_link'):
            df_hexroads.loc[df_hexroads['geo_h3_10'].isin([h3hex1, h3hex2]), 'secondary_link'] += 1
        if (df_roads['highway'][i] == 'tertiary'):
            df_hexroads.loc[df_hexroads['geo_h3_10'].isin([h3hex1, h3hex2]), 'tertiary'] += 1
        if (df_roads['highway'][i] == 'residential'):
            df_hexroads.loc[df_hexroads['geo_h3_10'].isin([h3hex1, h3hex2]), 'residential'] += 1
        if (df_roads['highway'][i] == 'motorway'):
            df_hexroads.loc[df_hexroads['geo_h3_10'].isin([h3hex1, h3hex2]), 'motorway'] += 1
        if (df_roads['highway'][i] == 'unclassified'):
            df_hexroads.loc[df_hexroads['geo_h3_10'].isin([h3hex1, h3hex2]), 'unclassified'] += 1
        df_hexroads.loc[df_hexroads['geo_h3_10'].isin([h3hex1, h3hex2]), 'city'] = df_roads['city'][i]
df_hexroads.to_csv('hexroads.csv')
