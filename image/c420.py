import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

H = [[0.299, 0.587, 0.114],
       [-0.169, -0.331, 0.500],
       [0.500, -0.419, -0.081]]

def c420(img):
  img = img.astype(np.float32)
  img_ycbcr = np.zeros(img.shape, dtype=np.float32)
  for i in range(img.shape[0]):
     for j in range(img.shape[1]):
        img_ycbcr[i][j] = np.reshape(H@np.reshape(img[i][j], (3, 1)), (1,3))
  img_ycbcr_com = img_ycbcr[0:-1:2, 0:-1:2, :]
  return img_ycbcr_com

if __name__ == "__main__":
    data = plt.imread("../test_image/PeppersRGB.bmp")
    data_com = c420(data)
    np.save('../buffer/Peppers.csv', data_com)