import numpy as np
import matplotlib.pyplot as plt
from c420 import H

def c420_decom(img_ycbcr_com):
  img_ycbcr_com_rgb = np.zeros(img_ycbcr_com.shape, dtype=np.float32)
  for i in range(img_ycbcr_com.shape[0]):
     for j in range(img_ycbcr_com.shape[1]):
        img_ycbcr_com_rgb[i][j] = np.reshape(np.linalg.inv(H)@np.reshape(img_ycbcr_com[i][j], (3, 1)), (1,3))
  # img_ycbcr_com = img_ycbcr[0:-1:2, 0:-1:2, :]
  # return img_ycbcr_com

if __name__ == "__main__":
  img_ycbcr = np.load("../buffer/Peppers.npy")

  # print(arr.shape)
  
  # plt.imshow(data_com, cmap='gray', interpolation='nearest')
  # plt.imshow(data_com)
  # plt.colorbar()
  # plt.title('2D Array Visualization')
  # plt.show()
  # data_com.tofile("../buffer/Peppers.csv", sep = ',')
