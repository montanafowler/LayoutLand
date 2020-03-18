import cv2
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import argparse
import os


def getImageIds(directory):
    imageIds = []
    for filename in os.listdir(directory):
        print("filename " + filename)
        if "histagrams" in filename:
            print("skipping histagrams folder in loop")
            continue
        filenameSplitArray = filename.split(".")
        imageIds.append(filenameSplitArray[0])
    return imageIds


if __name__ == "__main__":

    # parse the folder with the app icons
    parser = argparse.ArgumentParser()
    parser.add_argument("--folder", help="image to be processed")
    args = parser.parse_args()
    if args.folder:
      filepath = args.folder

    if filepath is None:
      print ('ERROR! Need image to run prediction on. Please add --image <path_to_file>')
      exit(1)



    # dictionary with lists of the apps in the layout locations
    layoutMap = {}

    # get all the image imageIds
    imageIds = getImageIds(filepath)

    # fill the dictionary with all the spots & all the apps
    for r in range(3):
      for c in range(3):
          layoutMap[str(r) + "_" + str(c)] = imageIds #array to randomly select index

    # make a list of the popular apps that were detected, put rest in unidentified box
    popularApps = set()

    # go through and find the color pairs that cannot happen
    forbiddenPairs = {}

    # make a stack with good appSpots
    bestAppSpots = []

    # make a stack with rest, highest to lowest priority
    mediumAppSpots = []
    worstAppSpots = []

    #while the stacks have stuff
    while !bestAppSpots.empty() or !mediumAppSpots.empty() or !worstAppSpots.empty():
        if !bestAppSpots.empty():
            # randomly choose a good app if there are any, else a non good one

            # for all the neighbors
                # remove the forbidden pairs
                # if we made the list empty,,,
                    # restart
                    # add one to count
                    # print restarting
