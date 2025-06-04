import numpy as np
import matplotlib.pyplot as plt
# print("test")
# a=np.ones((4,4))
# ap = a[0:-1:2, 0:-1:2]
# print(a)
# print(ap)
# a = 102
# b = [int(i) for i in format(a, 'b')]
# print(b)
# print(b+1)
# a = 4.6
# b = round(a)
# print(type(b))
  # a = np.random.randint(0,8,(3,2,3), dtype=np.uint8)
  # print(a)
  # b = np.unpackbits(a)
  # print(b)
# a = np.reshape(a, (1,18))
# print(a)
# a = np.reshape(a, (3,2,3))
# print(a)

data = plt.imread("../test_image/PeppersRGB.bmp")
data2 = plt.imread("../test_image/Peppers_decom.bmp")

plt.imshow(data2-data, cmap='gray', interpolation='nearest')
# plt.colorbar()
# plt.title('2D Array Visualization')
plt.show()