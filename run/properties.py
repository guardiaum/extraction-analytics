import util.my_csv as csv
import util.constants as constants
import numpy as np
import statistics.geo_temp as prop
import pandas as pd
import util.input as inp
import sys

'''
    GROUP PROPERTIES COUNT
    It is required to inform categoriesName, 
    output file name, title for plot and subtitle if needed
'''


def timePropDict(categoriesName):
    timePropsDict = []

    for categoryName in categoriesName:
        print categoryName

        category = csv.readCSVFile(constants.infobox_datasets + "/" + categoryName)
        categoryName = categoryName.replace(".csv", "")

        articlesWithTimeProps = prop.getDateTimeProps(category)

        if (articlesWithTimeProps.shape[0] != 0):
            timeProps = prop.countDateTimeProps(category)

            timePropsDictAux = timeProps.to_dict()
            timePropsDictAux = timePropsDictAux.pop('Count')
            timePropsDictAux['Category'] = categoryName
            timePropsDict.append(timePropsDictAux)
    return timePropsDict

'''
    ITERATES THROUGH CATEGORIES DATASETS
'''
def geoPropDict(categoriesName):
    geoPropsDict = []

    for categoryName in categoriesName:
        print categoryName

        category = csv.readCSVFile(constants.infobox_datasets + "/" + categoryName)

        articlesWithGeoProps = prop.getGeoProps(category)

        if (articlesWithGeoProps.shape[1] != 0):
            geoProps = prop.countGeographicProps(category)

            geoPropsDictAux = geoProps.to_dict()
            geoPropsDictAux = geoPropsDictAux.pop('Count')
            geoPropsDictAux['Category'] = categoryName.replace(".csv", "")
            geoPropsDict.append(geoPropsDictAux)

    return geoPropsDict


def groupProps(propType, path, columns, filename, title):
    # Read datasets
    categoriesName = inp.readFiles(constants.infobox_datasets)

    if len(sys.argv) == 3:
        numberOfChunks = int(sys.argv[1])
        chunk2select = int(sys.argv[2]) - 1

        chunks = inp.chunkIt(categoriesName, numberOfChunks)

        categoriesName = chunks[chunk2select]

        print(chunks)
        print(categoriesName)

    propsDict = []
    if propType == 'geo':
        print("Generating geo properties statistics")
        propsDict = geoPropDict(categoriesName)
    elif propType == 'time':
        print("Generating temporal properties statistics")
        propsDict = timePropDict(categoriesName)

    categoriesResult = pd.DataFrame(propsDict, columns=columns)

    #v.groupPropsBarPlot(categoriesResult, "results/plots/"+filename+".png", title)
    categoriesResult.to_csv(path+filename+'.csv', index=False, header=True, sep=",")


# Geographic properties
columns = np.array(['Category','Latitude', 'Longitude', 'Coordinates', 'Location'])
groupProps(propType='geo', path='results/csv/', columns=columns,
           filename='geo-props-count', title="Spatial properties distribution")

# Datetime properties
columns = np.array(["Category", "Date", "Period", "Time"])
groupProps(propType='time', path='results/csv/', columns=columns,
           filename='time-props-count', title="Temporal properties distribution")