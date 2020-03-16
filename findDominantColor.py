import cv2
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import argparse
import os


def find_histogram(clt):
    """
    create a histogram with k clusters
    :param: clt
    :return:hist
    """
    numLabels = np.arange(0, len(np.unique(clt.labels_)) + 1)
    (hist, _) = np.histogram(clt.labels_, bins=numLabels)

    hist = hist.astype("float")
    hist /= hist.sum()

    return hist
def plot_colors2(hist, centroids):
    bar = np.zeros((50, 300, 3), dtype="uint8")
    startX = 0

    for (percent, color) in zip(hist, centroids):
        # plot the relative percentage of each cluster
        endX = startX + (percent * 300)
        cv2.rectangle(bar, (int(startX), 0), (int(endX), 50),
                      color.astype("uint8").tolist(), -1)
        startX = endX

    # return the bar chart
    return bar
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--image", help="image to be processed")
    args = parser.parse_args()

    if args.image:
      filepath = args.image

    if filepath is None:
      print ('ERROR! Need image to run prediction on. Please add --image <path_to_file>')
      exit(1)

    print("-----------------HISTAGRAM FILEPATH: " + filepath)
    img = cv2.imread(filepath)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    img = img.reshape((img.shape[0] * img.shape[1],3)) #represent as row*column,channel number
    clt = KMeans(n_clusters=3) #cluster number
    clt.fit(img)

    hist = find_histogram(clt)
    bar = plot_colors2(hist, clt.cluster_centers_)

    # make the histagrams folder in the folder with the image
    splitFilepath = filepath.split("\\")
    print("splitFilepath" + str(splitFilepath))
    if len(splitFilepath) <= 1:
        filepath = filepath.replace("/", "\\")
        splitFilepath = filepath.split("\\")
        print("splitFilepath" + str(splitFilepath))

    newFilepath = filepath.replace(splitFilepath[len(splitFilepath) - 1], "")
    newFilepath += "histagrams"
    if os.path.exists(newFilepath) == False:
        os.makedirs(newFilepath)

    # save the histagram with the image's name in the histagrams folder
    cv2.imwrite(newFilepath + "\\" + splitFilepath[len(splitFilepath) - 1], bar)
    print("new histagram: " + newFilepath + "\\" + splitFilepath[len(splitFilepath) - 1])
    # plt.axis("off")
    # plt.imshow(bar)
    # plt.show()
