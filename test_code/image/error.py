import numpy as np
import matplotlib.pyplot as plt

if __name__ == "__main__":
  img = plt.imread("../../test_image/Peppers_decom.bmp")
  golden = np.load("../../buffer/Peppers_bit.npy")
  emp = np.load("../../buffer/Peppers_bit_received.npy")
  print(img.size)
  # print(emp.shape)
  # print(golden.shape)
  L = 256
  W = 256
  emp = emp[range(golden.shape[0])]
  golden = np.reshape(golden, (L, W, -1))
  emp = np.reshape(emp, (L, W, -1))


  error = np.zeros((golden.shape[0], golden.shape[1]))
  for i in range(error.shape[0]):
    for j in range(error.shape[1]):
      error[i][j] = np.sum(np.bitwise_xor(golden[i,j,:], emp[i,j,:]))

  # print(error[1,1:50])

  plt.figure()
  plt.subplot(1,2,1)
  plt.imshow(img)
  plt.subplot(1,2,2)
  plt.imshow(error, cmap='gray')
  plt.show()
