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


def processHistagrams(directory):
    histagramDir = directory + "//histagrams"
    if os.path.isdir(histagramDir) == False:
        print("ERROR: NO HISTAGRAM directory")
        exit(1)
    histagramDict = {}
    for filename in os.listdir(histagramDir):
        histagram = cv2.imread(histagramDir + "//" + filename, cv2.IMREAD_COLOR)
        cols = histagram.shape[1]
        print("shape: " + str(histagram.shape))

        img = cv2.cvtColor(histagram, cv2.COLOR_BGR2RGB)
        print("img cvt color: " + str(img[0,0]))
        colorKey = str(img[0,0][0]) + "," + str(img[0,0][1]) + "," + str(img[0,0][2])
        print("color_key " + str(colorKey))
        histagramColors = {}
        for j in range(cols):
            colorKey = str(img[0,j][0]) + "," + str(img[0,j][1]) + "," + str(img[0,j][2])
            if (colorKey in histagramColors.keys()) == False:
                histagramColors[colorKey] = 0
            histagramColors[colorKey] += 1
        print("histagramColors: " + str(histagramColors))




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
    processHistagrams(filepath)
    forbiddenPairs = {}

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
