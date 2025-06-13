import numpy as np
import matplotlib.pyplot as plt
import os, sys
import matlab.engine
from scipy.io import savemat
from scipy.io import loadmat
from image import bit_generator
filename = "Peppers"
com_img = np.load(f"../buffer/{filename}_com.npy")
bit_generator.bit_generator(com_img, filename)