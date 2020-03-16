import cv2
import numpy as np
import os.path
import argparse

from flask import Flask, request
from markupsafe import escape
from flask import render_template
app = Flask(__name__)
import base64
import random
import csv
import cv2
import os
IPHONE_7_DIMENSIONS = [750, 1334] #width, height
IPHONE_X_DIMENSIONS = [1125, 2436] #width, height
IPHONE_XS_MAX_DIMENSIONS = [1242, 2688] #width, height
UNDETECTED_PHONE_TYPE = "UNDETECTED"
IPHONE7 = "IPHONE7"
IPHONEX = "IPHONEX"
IPHONEXS_MAX = "IPHONEXS_MAX"
phoneType = UNDETECTED_PHONE_TYPE

ESC = 27


def segmentImage(pathToInput, imageName):
    #input screenshot
    homeScreen = cv2.imread(pathToInput)

    #make folder with name of screenshot if it doesn't exist
    splitFilenameArray = imageName.split(".")
    pathToOutput = "./data/" + splitFilenameArray[0]
    if len(splitFilenameArray) > 0 and not os.path.exists(pathToOutput):
        os.makedirs(pathToOutput)

    #get dimensions of screenshot
    dimensions = homeScreen.shape #height, width, channels
    print("dimensions: " + str(dimensions))

    #determine phone type
    phoneType = UNDETECTED_PHONE_TYPE
    if (dimensions[1] == IPHONE_7_DIMENSIONS[0]) and (dimensions[0] == IPHONE_7_DIMENSIONS[1]):
        phoneType = IPHONE7
    elif (dimensions[1] == IPHONE_X_DIMENSIONS[0]) and (dimensions[0] == IPHONE_X_DIMENSIONS[1]):
        phoneType = IPHONEX
    elif (dimensions[1] == IPHONE_XS_MAX_DIMENSIONS[0]) and (dimensions[0] == IPHONE_XS_MAX_DIMENSIONS[1]):
        phoneType = IPHONEXS_MAX

    print ("phone type: " + str(phoneType))

    frameSize = 110
    stepX = 175
    stepY = 175
    startCenter = [105, 120] #x, y

    #determine crop variables
    if phoneType == UNDETECTED_PHONE_TYPE:
        print("Phone type undetected, exit()")
        exit()
    if phoneType == IPHONE7:
        frameSize = 110
        stepX = 175
        stepY = 175
        startCenter = [105, 120] #x, y
    elif phoneType == IPHONEX:
        frameSize = 180
        stepX = 261
        stepY = 306
        startCenter = [171, 306]
        #startCenter = [81, 216]
    elif phoneType == IPHONEXS_MAX:
        frameSize = 195
        stepX = 290
        stepY = 335
        startCenter = [190, 330]
    else:
        exit()

    #initial center
    center = startCenter
    letters = ["A", "B", "C", "D", "E", "F"]
    for row in range(0, 6):
        for col in range(0, 4):
            # increment the center
            center = [startCenter[0] + col * stepX, startCenter[1] + row * stepY]

            # get the top left corner of the app to crop from
            cropX = int(center[0] - frameSize/2)
            cropY = int(center[1] - frameSize/2)

            # crop the image
            cropped = homeScreen[int(cropY):int(cropY+frameSize), int(cropX):int(cropX+frameSize)]

            # save the image
            imageFilename = letters[row] + str(col) + ".jpg"
            cv2.imwrite(pathToOutput + "/" + imageFilename, cropped)
            print ("saved " + pathToOutput + "/" + imageFilename)
            #cv2.imshow("cropped", cropped) #makes the icon pop up
            #cv2.waitKey(0)

    return pathToOutput

@app.route('/layoutLand', methods=['GET','POST'])
def layoutLand():
    # if we are initializing the page, just return the html
    if request.method == 'GET':
        return render_template("index.html", segmentedData={})

    # if we have received an image name then save it
    imageName = request.form['imageNameInput']
    print("imageName: " + str(imageName))

    pathToInput = "./data/" + imageName
    pathToOutput = "./data/output/" + imageName
    print("pathToInput = " + pathToInput)
    print("pathToOutput = " + pathToOutput)

    if os.path.isfile(pathToInput):
        segmentedImagesFolder = segmentImage(pathToInput, imageName)
        segmentedData = {}
        segmentedDataClassifications = []
        for filename in os.listdir(segmentedImagesFolder):

            print("filename " + filename)
            if "histagrams" in filename:
                print("skipping histagrams folder in loop")
                continue
            # encode the app icon into the array
            with open(segmentedImagesFolder + "/" + filename, "rb") as image_file:
                img = image_file.read()
                splitFilenameToGetCode = filename.split(".")
                segmentedData[splitFilenameToGetCode[0]] = base64.b64encode(img).decode('utf8')


            # classify the app icon
            newImageFilepath = segmentedImagesFolder + "/" + filename
            os.system("python classifier-builder-master\\run_model.py --image " + newImageFilepath)

            # time to read the classificationOutput
            with open("classificationOutput.txt", "r") as f:
                txt = f.read()
                print("text: " + txt)
                segmentedDataClassifications.append(txt)

            # process the histagram of the app icon
            os.system("python findDominantColor.py --image " + newImageFilepath)

        with open(pathToInput, "rb") as image_file:
            img = image_file.read()
            inputData = base64.b64encode(img)
    else:
        print("File not found!")
        return render_template("index.html", segmentedData={})

    if (phoneType == IPHONE7 or phoneType == IPHONEX or phoneType == IPHONEXS_MAX):
        rows = 6.0
        cols = 4.0
    else:
        rows = 6.0
        cols = 4.0

    appSpotSize = 100.0 / cols
    spotCountArray = []
    for i in range(int(rows) * int(cols)):
        spotCountArray.append(appSpotSize)
    print(spotCountArray)
    return render_template("index.html", text="temp text", segmentedData=segmentedData, segmentedDataClassifications=segmentedDataClassifications, inputData=inputData.decode('utf8'), rows=rows, cols=cols)
