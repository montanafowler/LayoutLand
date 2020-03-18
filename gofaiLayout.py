import cv2
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import argparse
import os





if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--folder", help="image to be processed")
    args = parser.parse_args()

    if args.folder:
      filepath = args.folder

    if filepath is None:
      print ('ERROR! Need image to run prediction on. Please add --image <path_to_file>')
      exit(1)
