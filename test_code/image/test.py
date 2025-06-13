import numpy as np
import matplotlib.pyplot as plt
import os, sys
import matlab.engine
from scipy.io import savemat
from scipy.io import loadmat

a = np.load("../../buffer/Peppers_com.npy")
b = np.load("../../buffer/Peppers_bit.npy")
c = np.load("../../buffer/Peppers_bit_received.npy")
d = np.load("../../buffer/Peppers_com_received.npy")
print(a.shape)
print(b.shape)
print(c.shape)
print(d.shape)