###################################################
# Skin Cancer Preprocessing Module                #
# by Arseniy Arsentyev (programpro.ars@gmail.com) #
###################################################
from skimage.color import rgb2gray
from skimage.filters import threshold_isodata
from skimage.io import imread
import scipy.ndimage as ndi
from collections import deque
import numpy as np


class Coefficients:
    """ A class which is used to calculate coefficients for skin classification """

    def __init__(self, image_path):
        """
        Perform all calculations

        Parameters
        ----------
        image_path: str
            The absolute path to the image file
        """
        # load image from file
        self.img = imread(image_path)
        # transform image to grayscale
        self.gray_image = rgb2gray(self.img)
        # Perform thresholding
        self.threshold = self.gray_image > threshold_isodata(self.gray_image)
        # Clear image from hair
        self.mask = ndi.binary_closing(self.threshold, iterations=17)
        self.mask = ndi.binary_erosion(self.mask, iterations=10)
        # Delete field's borders
        self.delete_border()
        # Save resulting coefficients
        self.coefficients = [self.calculate_radius(), self.calculate_color(), self.calculate_size()]

    def delete_border(self):
        """ Delete the image border """
        queue = deque([[0, 0]])

        while len(queue) != 0:
            tp = queue.popleft()
            if self.mask[tp[0]][tp[1]]:
                continue

            self.mask[tp[0]][tp[1]] = True
            comp_tp_0 = (tp[0] < self.mask.shape[0] - 1)
            comp_tp_1 = (tp[1] < self.mask.shape[1] - 1)
            if tp[0] > 0 and not (self.mask[tp[0] - 1][tp[1]]):
                queue.append([tp[0] - 1, tp[1]])
            if comp_tp_0 and not (self.mask[tp[0] + 1][tp[1]]):
                queue.append([tp[0] + 1, tp[1]])
            if tp[1] > 0 and not (self.mask[tp[0]][tp[1] - 1]):
                queue.append([tp[0], tp[1] - 1])
            if comp_tp_1 and not (self.mask[tp[0]][tp[1] + 1]):
                queue.append([tp[0], tp[1] + 1])
            if tp[0] > 0 and tp[1] > 0 and not (self.mask[tp[0] - 1][tp[1] - 1]):
                queue.append([tp[0] - 1, tp[1] - 1])
            if comp_tp_0 and comp_tp_1 and not (self.mask[tp[0] + 1][tp[1] + 1]):
                queue.append([tp[0] + 1, tp[1] + 1])
            if tp[0] > 0 and comp_tp_1 and not (self.mask[tp[0] - 1][tp[1] + 1]):
                queue.append([tp[0] - 1, tp[1] + 1])
            if tp[1] > 0 and comp_tp_0 and not (self.mask[tp[0] + 1][tp[1] - 1]):
                queue.append([tp[0] + 1, tp[1] - 1])

    def calculate_radius(self):
        """ Calculate the maximum radius of the skin lesions """
        if np.all(self.mask):
            self.mask = np.copy(self.threshold)
        previous_mask = np.copy(self.mask)
        max_cluster = 0
        for i in range(self.mask.shape[0]):
            for j in range(self.mask.shape[1]):
                if self.mask[i][j]:
                    continue
                current_cluster = 0
                queue = deque([[i, j]])
                while len(queue) != 0:
                    tp = queue.popleft()
                    if self.mask[tp[0]][tp[1]]:
                        continue
                    self.mask[tp[0]][tp[1]] = True
                    current_cluster += 1
                    comp_tp_0 = (tp[0] < self.mask.shape[0] - 1)
                    comp_tp_1 = (tp[1] < self.mask.shape[1] - 1)
                    if tp[0] > 0 and not (self.mask[tp[0] - 1][tp[1]]):
                        queue.append([tp[0] - 1, tp[1]])
                    if comp_tp_0 and not (self.mask[tp[0] + 1][tp[1]]):
                        queue.append([tp[0] + 1, tp[1]])
                    if tp[1] > 0 and not (self.mask[tp[0]][tp[1] - 1]):
                        queue.append([tp[0], tp[1] - 1])
                    if comp_tp_1 and not (self.mask[tp[0]][tp[1] + 1]):
                        queue.append([tp[0], tp[1] + 1])
                    if tp[0] > 0 and tp[1] > 0 and not (self.mask[tp[0] - 1][tp[1] - 1]):
                        queue.append([tp[0] - 1, tp[1] - 1])
                    if comp_tp_0 and comp_tp_1 and not (self.mask[tp[0] + 1][tp[1] + 1]):
                        queue.append([tp[0] + 1, tp[1] + 1])
                    if tp[0] > 0 and comp_tp_1 and not (self.mask[tp[0] - 1][tp[1] + 1]):
                        queue.append([tp[0] - 1, tp[1] + 1])
                    if tp[1] > 0 and comp_tp_0 and not (self.mask[tp[0] + 1][tp[1] - 1]):
                        queue.append([tp[0] + 1, tp[1] - 1])
                max_cluster = max(max_cluster, current_cluster)
        coefficient = max_cluster / float(self.mask.shape[0] * self.mask.shape[1])
        self.mask = previous_mask
        return coefficient

    def calculate_color(self):
        """ Calculate color coefficient of the skin lesion """
        self.img = self.img.astype(np.uint16)
        avg = np.mean(np.mean(self.img, axis=0))
        avg *= 3
        max_diff = 0
        for i in range(self.mask.shape[0]):
            for j in range(self.mask.shape[1]):
                if not (self.mask[i][j]):
                    max_diff = max(max_diff, abs(avg - (self.img[i][j][0] + self.img[i][j][1] + self.img[i][j][2])))
        return max_diff * 0.00130718954

    def calculate_size(self):
        """ Calculate size coefficient of the skin lesion """
        left, right, top, bottom = 10000, 0, 0, 10000
        for i in range(self.mask.shape[0]):
            for j in range(self.mask.shape[1]):
                if not (self.mask[i][j]):
                    left = min(i, left)
                    right = max(i, right)
                    bottom = min(j, bottom)
                    top = max(j, top)
        if left == 10000:
            return 0.0
        return ((right - left) * (top - bottom)) / float(self.mask.shape[0] * self.mask.shape[1])

    def get_coefficients(self):
        """ Return list of the coefficients """
        return self.coefficients

    def get_threshold_image(self):
        """ Return threshold image """
        return self.threshold

    def get_mask_image(self):
        """ Return mask image """
        return self.mask


# If program is used in console, show simple CLI
if __name__ == '__main__':
    path = input('Path to the image: ')
    print('------------------')
    to_print = Coefficients(path).get_coefficients()
    print('Radius:', to_print[0])
    print('Color:', to_print[1])
    print('Size:', to_print[2])
