import cv2
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import argparse
import os

def processIdFromImageName(imageName):
    filenameSplitArray = imageName.split(".")
    return filenameSplitArray[0]

def getImageIds(directory):
    imageIds = []
    for filename in os.listdir(directory):
        if "histagrams" in filename:
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
                #if abs(colorDict0[key0] - colorDict1[key1]) < 28:
                #if (float(colorDict0[key0]) / 300.0)
                color0Percentage = float(colorDict0[key0]) / 300.0 * 100.0
                color1Percentage = float(colorDict1[key1]) / 300.0 * 100.0

                if (abs(color0Percentage - color1Percentage) < 10.0):
                    print ("color0 percentage " + str(float(colorDict0[key0]) / 300.0))
                    print ("color1 percentage " + str(float(colorDict1[key1]) / 300.0))
                    return True
    return False


def cleanUpHistagramColorDictionary(histagramColors):
    entriesToDelete = []
    for key in histagramColors.keys():
        if histagramColors[key] < 90:
            entriesToDelete.append(key)
    for entry in entriesToDelete:
        histagramColors.pop(entry)
    print("histagramColors cleaned up: " + str(histagramColors))
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

    print("histagramDict " + str(histagramDict))
    forbiddenPairs = {}
    count = 0
    for k0 in histagramDict.keys():
        for k1 in histagramDict.keys():
            similarity = appColorsAreSimilar(histagramDict[k0], histagramDict[k1])
            if similarity:
                if k0 != k1:
                    print(k0 + " and " + k1 + " are similar: " + str(similarity))
                    count += 1
                    # if the keys are not already in forbidden pairs, initialize sets
                    if (k0 in forbiddenPairs.keys()) == False:
                        forbiddenPairs[k0] = set()
                    if (k1 in forbiddenPairs.keys()) == False:
                        forbiddenPairs[k1] = set()

                    # add each to the set
                    forbiddenPairs[k0].add(k1)
                    forbiddenPairs[k1].add(k0)
    print ("count " + str(count/2))
    return forbiddenPairs

def isEmpty(stack):
    return len(stack) == 0

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



    # dictionary with lists of the apps in the layout locations
    layoutMap = {}

    # get all the image imageIds
    imageIds = getImageIds(filepath)
    print(imageIds)

    # fill the dictionary with all the spots & all the apps
    for r in range(3):
      for c in range(3):
          layoutMap[str(r) + "_" + str(c)] = imageIds #array to randomly select index

    # make a list of the popular apps that were detected, put rest in unidentified box
    popularApps = set()

    # go through and find the color pairs that cannot happen
    forbiddenPairs = processHistagrams(filepath)
    print(forbiddenPairs)

    # make a stack with good appSpots
    bestAppSpots = []

    # make a stack with rest, highest to lowest priority
    mediumAppSpots = []
    worstAppSpots = []

    #while the stacks have stuff
    while (isEmpty(bestAppSpots) and isEmpty(mediumAppSpots) and isEmpty(worstAppSpots)) == False:
        if isEmpty(bestAppSpots) == False:
            print("best apps not empty")
            # randomly choose a good app if there are any, else a non good one

            # for all the neighbors
                # remove the forbidden pairs
                # if we made the list empty,,,
                    # restart
                    # add one to count
                    # print restarting
