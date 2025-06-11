import numpy as np
import matplotlib.pyplot as plt
import os
import cv2

H = np.array([[0.299, 0.587, 0.114],
       [-0.169, -0.331, 0.500],
       [0.500, -0.419, -0.081]])

def c420_decom(img_ycbcr_com, filename):
  Hp = np.linalg.inv(H)
  img_ycbcr_com_rgb = np.zeros(img_ycbcr_com.shape, dtype=np.float32)
  for i in range(img_ycbcr_com.shape[0]):
     for j in range(img_ycbcr_com.shape[1]):
        img_ycbcr_com_rgb[i][j] = np.reshape(Hp@np.reshape(img_ycbcr_com[i][j], (3, 1)), (1,3))
  img_ycbcr_com_rgb_decom = cv2.resize(img_ycbcr_com_rgb, (0, 0), fx=2, fy=2, interpolation=cv2.INTER_LINEAR)
  img_ycbcr_com_rgb_decom = np.clip(img_ycbcr_com_rgb_decom/255, 0, 1)
  plt.imsave(os.path.join(os.path.dirname(__file__), f"../../test_image/{filename}_decom.bmp"), img_ycbcr_com_rgb_decom)
  return

if __name__ == "__main__":
  data = np.load("./../../buffer/Pepper_com_quantized.npy")
  c420_decom(data, "Peppers_quantized")
  
