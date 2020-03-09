
import cv2
import os
IPHONE_7_DIMENSIONS = [750, 1334] #width, height
IPHONE_X_DIMENSIONS = [1125, 2436] #width, height
IPHONE_XS_MAX_DIMENSIONS = [1242, 2688] #width, height
UNDETECTED_PHONE_TYPE = "UNDETECTED"
IPHONE7 = "IPHONE7"
IPHONEX = "IPHONEX"
IPHONEXS_MAX = "IPHONEXS_MAX"

#input screenshot
inputFilename = "montana.png"
homeScreen = cv2.imread("../data/" + inputFilename)

#make folder with name of screenshot if it doesn't exist
splitFilenameArray = inputFilename.split(".")
if len(splitFilenameArray) > 0 and not os.path.exists("../data/" + splitFilenameArray[0]):
    os.makedirs("../data/" + splitFilenameArray[0])

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
    startCenter = [175, 300]
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
        cv2.imwrite("../data/" + splitFilenameArray[0] + "/" + imageFilename, cropped)
        print ("saved " + "../data/" + splitFilenameArray[0] + "/" + imageFilename)
        #cv2.imshow("cropped", cropped) #makes the icon pop up
        #cv2.waitKey(0)


#crop_img = img[y:y+h, x:x+w]




# Using cv2.imread() method
# to read the image
#img = cv2.imread(image_path)

# Change the current directory
# to specified directory
#os.chdir(directory)

# List files and directories
# in 'C:/Users/Rajnish/Desktop/GeeksforGeeks'
#print("Before saving image:")
#print(os.listdir(directory))

# Filename
#filename = 'savedImage.jpg'

# Using cv2.imwrite() method
# Saving the image
#cv2.imwrite(filename, img)
