import numpy as np
import matplotlib.pyplot as plt
import os
# from c420 import H
# a = np.array([[1,2,3],[4,5,6]])
# b = (a-128)*2
# print(b)
# H = np.array([[0.299, 0.587, 0.114],
#        [-0.169, -0.331, 0.500],
#        [0.500, -0.419, -0.081]])
# print(np.linalg.inv(H))
# a = np.load("../../buffer/Peppers_com.npy")
# b = np.round(a)
# np.save(os.path.join(os.path.dirname(__file__), f"../../buffer/Pepper_com_quantized.npy"), b)
# a = [1,0,0,1]
# b = [0,1,0,1]
# print(np.bitwise_xor(a,b))
# a = np.array([[1,2],[3,4]])
# print(np.linalg.norm(a))
# a = np.array([1,2,3,4])
# b = [3,4]
# c = 1
# print(np.multiply(a,b))
# print(a-c)
a = np.load("../../buffer/Peppers_com.npy")
print(a.shape)