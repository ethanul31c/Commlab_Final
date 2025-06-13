import numpy as np
import matplotlib.pyplot as plt
import os, sys
import matlab.engine
from scipy.io import savemat
from scipy.io import loadmat


# try:
#     sess = matlab.engine.start_matlab("")
#     print("MATLAB 啟動成功！")
# except Exception as e:
#     print("MATLAB 啟動失敗：", str(e))
#     sys.exit(1)  # 非 0 表示異常退出，程式會停止在這裡

# sess.cd(os.getcwd())
# sum = sess.add(1,2)
# print(sum)
a = np.array([1,2,3])
b = np.array([4,5,6])
# print(type(a))
np.savez("./testt.npz", a=a, b=b)
c = np.load("./testt.npz")
# print(c)
print(c['a'])
print(c['b'])