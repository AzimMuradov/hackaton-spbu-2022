import pandas as pd
import h3

df_companies = pd.read_csv("osm_amenity.csv")                     
df_companies = df_companies.fillna('')

neighbors = pd.DataFrame(data=df_companies['geo_h3_10'])
neighbors['firstLayer'] = [''] * neighbors.shape[0]
neighbors['secondLayer'] = [''] * neighbors.shape[0]
hexes = neighbors['geo_h3_10']
for i in range(neighbors.shape[0]):
    fLayerIndex = ''
    fSecondLayerIndex = ''
    firstLayer = h3.hex_ring(hexes[i], 1)
    secondLayer = h3.hex_ring(hexes[i], 2)
    for j in firstLayer:
        neighbor = neighbors.index[neighbors['geo_h3_10'] == j]
        if (not neighbor.empty):
            fLayerIndex += (str(neighbor.tolist()[0]) + ' ')
        else:
            fLayerIndex += '-1 '
    for j in secondLayer:
        neighbor = neighbors.index[neighbors['geo_h3_10'] == j]
        if (not neighbor.empty):
            fSecondLayerIndex += (str(neighbor.tolist()[0]) + ' ')
        else:
            fSecondLayerIndex += '-1 '
    neighbors['firstLayer'][i] = fLayerIndex
    neighbors['secondLayer'][i] = fSecondLayerIndex
neighbors.to_csv('neighbors.csv')
