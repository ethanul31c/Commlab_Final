import matplotlib.pyplot as plt
import numpy as np
import os

H = np.array([[0.299, 0.587, 0.114],
       [-0.169, -0.331, 0.500],
       [0.500, -0.419, -0.081]])

def c422(img, filename):
  img = img.astype(np.float32)
  img_ycbcr = np.zeros(img.shape, dtype=np.float32)
  for i in range(img.shape[0]):
     for j in range(img.shape[1]):
        img_ycbcr[i][j] = np.reshape(H@np.reshape(img[i][j], (3, 1)), (1,3))
  img_ycbcr_com = img_ycbcr[:, 0:-1:2, :]
  np.save(os.path.join(os.path.dirname(__file__), f'../../buffer/{filename}_com.npy'), img_ycbcr_com)
  return img_ycbcr_com

if __name__ == "__main__":
    data = plt.imread("../../test_image/Peppers.bmp")
    data_com = c422(data, "Peppers")