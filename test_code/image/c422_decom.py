import numpy as np
import matplotlib.pyplot as plt
import cv2 

H = np.array([[0.299, 0.587, 0.114],
       [-0.169, -0.331, 0.500],
       [0.500, -0.419, -0.081]])

def c420_decom(img_ycbcr_com):
  Hp = np.linalg.inv(H)
  img_ycbcr_com_rgb = np.zeros(img_ycbcr_com.shape, dtype=np.float32)
  for i in range(img_ycbcr_com.shape[0]):
     for j in range(img_ycbcr_com.shape[1]):
        img_ycbcr_com_rgb[i][j] = np.reshape(Hp@np.reshape(img_ycbcr_com[i][j], (3, 1)), (1,3))
  img_ycbcr_com_rgb_decom = cv2.resize(img_ycbcr_com_rgb, (0, 0), fx=2, fy=1, interpolation=cv2.INTER_LINEAR)
  return img_ycbcr_com_rgb_decom

if __name__ == "__main__":
  data = np.load("../buffer/Peppers_com_received.npy")
  data_decom = c420_decom(data)
  data_decom = np.clip(data_decom/255, 0, 1)
  plt.imsave("../test_image/Peppers_decom.bmp", data_decom)
