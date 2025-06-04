import numpy as np
import matplotlib.pyplot as plt
from c420 import H
import cv2 
def c420_decom(img_ycbcr_com):
  img_ycbcr_com_rgb = np.zeros(img_ycbcr_com.shape, dtype=np.float32)
  for i in range(img_ycbcr_com.shape[0]):
     for j in range(img_ycbcr_com.shape[1]):
        img_ycbcr_com_rgb[i][j] = np.reshape(np.linalg.inv(H)@np.reshape(img_ycbcr_com[i][j], (3, 1)), (1,3))
  img_ycbcr_com_rgb_decom = cv2.resize(img_ycbcr_com_rgb, (0, 0), fx=2, fy=2, interpolation=cv2.INTER_LINEAR)/255
  return img_ycbcr_com_rgb_decom

if __name__ == "__main__":
  data = np.load("../buffer/Peppers.npy")
  data_decom = c420_decom(data)
  # print(arr.shape)
  
  plt.imshow(data_decom, cmap='gray', interpolation='nearest')
  plt.colorbar()
  # plt.title('2D Array Visualization')
  plt.show()
