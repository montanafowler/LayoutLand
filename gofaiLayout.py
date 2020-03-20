import cv2
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import argparse
import os
import random
import json

def shuffleArray(arr):
    for i in range(len(arr)):
        randomIndex = int(random.random() * len(arr))
        temp = arr[i]
        arr[i] = arr[randomIndex]
        arr[randomIndex] = temp
    return arr

def processIdFromImageName(imageName):
    filenameSplitArray = imageName.split(".")
    return filenameSplitArray[0]

def getImageIds(directory):
    imageIds = []
    for filename in os.listdir(directory):
        if "histagrams" in filename or "classifications" in filename or "layout" in filename or "forbidden" in filename:
            continue
        imageIds.append(processIdFromImageName(filename))
    return imageIds

def appColorsAreSimilar(colorDict0, colorDict1):
    for key0 in colorDict0.keys():
        for key1 in colorDict1.keys():
            color0 = key0.split(',')
            color1 = key1.split(',')
            colorDifference = [int(color0[0]) - int(color1[0]), int(color0[1]) - int(color1[1]), int(color0[2]) - int(color1[2])]
            # if all three channels are withing +- 15 of each other
            if abs(colorDifference[0]) < 15 and abs(colorDifference[1]) < 15 and abs(colorDifference[2]) < 15:
                color0Percentage = float(colorDict0[key0]) / 300.0 * 100.0
                color1Percentage = float(colorDict1[key1]) / 300.0 * 100.0
                # if the percentage difference is +-10
                if (abs(color0Percentage - color1Percentage) < 10.0):
                    return True
    return False

def cleanUpHistagramColorDictionary(histagramColors):
    entriesToDelete = []
    for key in histagramColors.keys():
        if histagramColors[key] < 90:
            entriesToDelete.append(key)
    for entry in entriesToDelete:
        histagramColors.pop(entry)
    #print("histagramColors cleaned up: " + str(histagramColors))
    return histagramColors

def fillHistagramColorDictionary(cols, histagram):
    histagramColors = {}
    # fill histagram colors with all the colors
    for j in range(cols):
        colorKey = str(histagram[0,j][0]) + "," + str(histagram[0,j][1]) + "," + str(histagram[0,j][2])
        if (colorKey in histagramColors.keys()) == False:
            histagramColors[colorKey] = 0
        histagramColors[colorKey] += 1
    return histagramColors

def processHistagrams(directory):
    histagramDir = directory + "//histagrams"
    if os.path.isdir(histagramDir) == False:
        print("ERROR: NO HISTAGRAM directory")
        exit(1)
    histagramDict = {}
    for filename in os.listdir(histagramDir):
        histagram = cv2.imread(histagramDir + "//" + filename, cv2.IMREAD_COLOR)
        histagram = cv2.cvtColor(histagram, cv2.COLOR_BGR2RGB)
        cols = histagram.shape[1]

        # fill histagram colors with all the colors
        histagramColors = fillHistagramColorDictionary(cols, histagram)

        # delete the entries that don't dominate
        histagramColors = cleanUpHistagramColorDictionary(histagramColors)

        # add the dictionary to the full collection
        histagramDict[processIdFromImageName(filename)] = histagramColors

    #print("histagramDict " + str(histagramDict))
    forbiddenPairs = {}
    count = 0
    for k0 in histagramDict.keys():
        for k1 in histagramDict.keys():
            similarity = appColorsAreSimilar(histagramDict[k0], histagramDict[k1])
            if similarity:
                if k0 != k1:
                    #print(k0 + " and " + k1 + " are similar: " + str(similarity))
                    count += 1
                    # if the keys are not already in forbidden pairs, initialize sets
                    if (k0 in forbiddenPairs.keys()) == False:
                        forbiddenPairs[k0] = set()
                    if (k1 in forbiddenPairs.keys()) == False:
                        forbiddenPairs[k1] = set()

                    # add each to the set
                    forbiddenPairs[k0].add(k1)
                    forbiddenPairs[k1].add(k0)
    #print ("count " + str(count/2))
    return forbiddenPairs

def isEmpty(stack):
    return len(stack) == 0

def processClassificatons(directory):
    classificationDict = {}
    classificationsSet = set()
    with open(directory + "\\classifications.txt", "r") as f:
        txt = f.read()
        newLineSplit = txt.split('\n')

    for i in range(len(newLineSplit) - 1):
        commaSplit = newLineSplit[i].split(',')
        dashSplit = commaSplit[1].split(' - ')
        if(float(dashSplit[1]) > 0.6):
            classificationDict[commaSplit[0]] = dashSplit[0]
        else:
            classificationDict[commaSplit[0]] = "unknown"
        classificationsSet.add(classificationDict[commaSplit[0]])
    return [classificationDict, classificationsSet]

def seedIndexArray(length):
    arr = []
    for i in range(length):
        arr.append(i)
    return shuffleArray(arr)

def randomlySelectGoodApp(layoutMap, appSpot, classificationDict, topApps):
    indices = seedIndexArray(len(layoutMap[appSpot]))
    for i in range(len(indices)):
        app = layoutMap[appSpot][indices[i]]
        #print("app is " + app)
        if (classificationDict[app] in topApps):
            break
    return app

def removeAllForbiddenAppsFromNeighbors(R, C, appsToRemove, layoutMap):
    # for all the neighbors
    for r in range(-1, 2):
        for c in range(-1, 2):
            #print("\t\t\tr, c " + str(r) + ", " + str(c))
            # only do left, right, top and bottom
            if r != c and (R + r) > 0 and (R + r) < 6 and (C + c) > 0 and (C + c) < 4:
                # for each app to remove
                for a in appsToRemove:
                    #print("\t\t\t\tapp to remove: " + a)
                    #print("\t\t\t\tlayoutMap[" + str(R + r) + "_" + str(C + c) + "] = " + str(layoutMap[str(R + r) + "_" + str(C + c)]))
                    # if the app is in the list, remove it
                    if(a in layoutMap[str(R + r) + "_" + str(C + c)]):
                        layoutMap[str(R + r) + "_" + str(C + c)].remove(a)
                        #print("\t\t\t\t\tremoved: layoutMap[" + str(R + r) + "_" + str(C + c) + "] = " + str(layoutMap[str(R + r) + "_" + str(C + c)]))
                        # if we made the list empty: error WE GOTTA TRY again
                        if len(layoutMap[str(R + r) + "_" + str(C + c)]) == 0:
                            print("WE MADE AN APP SPOT HAVE NO OPTIONS UH OH")
                            return None
    return layoutMap

def makeAppExclusiveForAppSpot(app, appSpot, layoutMap):
    for k in layoutMap.keys():
        #print("\tk " + str(k) + " app: " + app)
        if k != appSpot:
            if app in layoutMap[k]:
                layoutMap[k].remove(app)
                #print("\t\tremoved LayoutMap[" + str(k) + "] = " + str(layoutMap[k]))
                if len(layoutMap[k]) == 0:
                    print("WE MADE AN APP SPOT HAVE NO OPTIONS UH OH")
                    return None # trigger failed try
        else:
            layoutMap[appSpot] = [app] #make it the only item in there
            #print("\t\tremoved LayoutMap[" + str(k) + "] = " + str(layoutMap[k]))
    return layoutMap

def fitLayout(bestAppSpots, mediumAppSpots, worstAppSpots, classificationDict, topApps, imageIds, forbiddenPairs):
    # shuffle arrays
    bestAppSpots = shuffleArray(bestAppSpots)
    mediumAppSpots = shuffleArray(mediumAppSpots)
    worstAppSpots = shuffleArray(worstAppSpots)
    appSpots = worstAppSpots + mediumAppSpots + bestAppSpots # combine lists once they have been shuffled

    # fill the dictionary with all the spots & all the apps
    # dictionary with lists of the apps in the layout locations
    layoutMap = {}
    for r in range(6):
      for c in range(4):
          layoutMap[str(r) + "_" + str(c)] = imageIds.copy() #array to randomly select index

    #while the stacks have stuff
    while isEmpty(appSpots) == False: #and isEmpty(mediumAppSpots) and isEmpty(worstAppSpots)) == False:
        if isEmpty(appSpots) == False:
            appSpot = appSpots.pop()
            parsedAppSpot = appSpot.split("_")
            #print("appSpot: " + appSpot)

            # randomly choose a good app if there are any, else a non good one
            app = randomlySelectGoodApp(layoutMap, appSpot, classificationDict, topApps)
            #print("\tselected app: " + app + " classified as " + classificationDict[app] + " for " + appSpot)

            #print("\tapp in forbiddenPairs: " + str(app in forbiddenPairs.keys()))
            # if there are pairs to remove
            if (app in forbiddenPairs.keys()):
                appsToRemove = forbiddenPairs[app]
                R = int(parsedAppSpot[0])
                C = int(parsedAppSpot[1])
                #print("\t\t" + app + " in forbidden pairs for " + str(appsToRemove))

                # remove forbidden pairs from all the neighbors
                layoutMap = removeAllForbiddenAppsFromNeighbors(R, C, appsToRemove, layoutMap)
                if layoutMap == None:
                    return None # failed try trigger

            # remove the app from every other list and clear list except for app
            layoutMap = makeAppExclusiveForAppSpot(app, appSpot, layoutMap)
            if layoutMap == None:
                return None # failed try trigger
    return layoutMap

if __name__ == "__main__":

    # parse the folder with the app icons
    parser = argparse.ArgumentParser()
    parser.add_argument("--folder", help="image to be processed")
    args = parser.parse_args()
    if args.folder:
      filepath = args.folder
      print(filepath)

    if filepath is None:
      print ('ERROR! Need image to run prediction on. Please add --image <path_to_file>')
      exit(1)

    # get all the image imageIds
    imageIds = getImageIds(filepath)

    # make a list of the popular apps that were detected, put rest in unidentified box
    popularApps = set()

    # go through and find the color pairs that cannot happen
    forbiddenPairs = processHistagrams(filepath)
    #print(forbiddenPairs)

    #top apps of 2019 with added default apple ones
    topApps = set(['youtube', 'television', 'instagram', 'snapchat', 'tiktok', 'messenger', 'gmail', 'netflix', 'facebook', 'maps', 'amazon', 'spotify', 'doordash', 'whatsapp', 'faceapp', 'uber', 'yolo', 'hulu', 'venmo', 'bitmoji', 'chrome'])
    topApps = topApps.union(set(['messages', 'mail', 'safari', 'camera', 'photos', 'phone', 'facetime', 'video camera', 'music', 'calendar', 'weather', 'podcasts', 'clock', 'settings', 'reminder']))

    #process classifications
    classificationDictAndSet = processClassificatons(filepath)
    classificationDict = classificationDictAndSet[0]
    classificationsSet = classificationDictAndSet[1]

    # remove top apps not detected in home screen
    topApps = topApps.intersection(classificationsSet)
    print("topApps " + str(topApps))

    # gather the non-top apps
    nonTopApps = classificationsSet.difference(topApps)
    print("nonTopApps " + str(nonTopApps))

    # make a stack with good appSpots
    bestAppSpots = ['3_2', '3_3', '4_2', '4_3', '5_2', '5_3', '3_1', '4_1']
    mediumAppSpots = ['3_0', '4_0', '5_0', '5_1', '2_0', '2_1', '2_2', '2_3', '1_3', '1_2']
    worstAppSpots = ['1_0', '1_1', '0_0', '0_1', '0_2', '0_3']

    for i in range(20):
        layoutMap = fitLayout(bestAppSpots, mediumAppSpots, worstAppSpots, classificationDict, topApps, imageIds, forbiddenPairs)
        if layoutMap != None:
            print ("try #" + str(i))
            break

    print("FINAL LAYOUTMAP: " + str(layoutMap))
    with open(filepath + "\\layout.txt", "w+") as layoutFile:
        layoutFile.write(json.dumps(layoutMap))

    with open(filepath + "\\forbiddenPairs.txt", "w+") as forbiddenPairsFile:
        forbiddenPairsFile.write(json.dumps(forbiddenPairs))
