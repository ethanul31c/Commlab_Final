import matlab.engine
from scipy.io import savemat
from scipy.io import loadmat
import numpy as np
import sys


try:
    sess = matlab.engine.start_matlab("")
    print("MATLAB 啟動成功！")
except Exception as e:
    print("MATLAB 啟動失敗：", str(e))
    sys.exit(1)  # 非 0 表示異常退出，程式會停止在這裡




sess.cd(r'C:\\Users\\Ethan\\Desktop\\USRP\\Final\\Commlab_Final\\test_code')


# a = sess.add(5.0, 9.0)
# print(type(a))
# print(a)
# (status, info) = sess.findsdru(nargout=2)
# print("Status:", status)
# print("Info:", info)
sess.test_one_frame(nargout=0)

data = loadmat('received_test.mat')
print(data.keys())   # 包含 __header__, __globals__, a, b...
print(f'ofdm_start read by python = ', data['ofdm_start'])     # 取出 MATLAB 中的 a
# print(type(received_buffer))
# print(received_buffer)

input("請按 Enter 結束...")

