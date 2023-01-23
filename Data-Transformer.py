###################################################
# Data Transformation Module                      #
# by Arseniy Arsentyev (programpro.ars@gmail.com) #
###################################################
import os
import multiprocessing
import numpy as np
import pandas as pd
from skimage.io import imread
from skimage.transform import resize

# Determine number of CPU cores
workers_count = multiprocessing.cpu_count()

path_to_ISIC_dataset = '/Users/b_arsick/Desktop/dataset-melanoma'
path_to_data = path_to_ISIC_dataset + '/train'
path_to_csv = path_to_ISIC_dataset + '/train.csv'

# Load data
data = os.listdir(path_to_data)
label_csv = pd.read_csv(path_to_csv)


def worker(name):
    # Resize and convert image to the NN training format
    try:
        img = imread(path_to_data + '/' + str(name))
        img = resize(img, (512, 512))
        img = 255 * img
        img = img.astype(np.uint8)
        arr = np.array([img])
        return arr
    except:
        return np.zeros((512, 512, 3))


if __name__ == '__main__':
    images = os.listdir(path_to_data)
    labels = []
    for image in images:
        try:
            labels.append(label_csv[label_csv['image_name'] == image[:-4]].target)
        except:
            labels.append(0)
    np.save('labels.npy', labels)

    # Apply 'worker' function for every image using parallel computation
    with multiprocessing.Pool(processes=workers_count) as p:
        data = np.array(p.map(worker, os.listdir(path_to_data)))
        np.save('data.npy', data)
