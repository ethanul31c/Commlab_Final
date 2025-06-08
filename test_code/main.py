import matlab.engine
from scipy.io import savemat
from scipy.io import loadmat
import numpy as np
import sys
import os

USE_USRP = 1
QAM_SIZE = 64

try:
    sess = matlab.engine.start_matlab("")
    print("MATLAB 啟動成功！")
except Exception as e:
    print("MATLAB 啟動失敗：", str(e))
    sys.exit(1)  # 非 0 表示異常退出，程式會停止在這裡

sess.cd(os.getcwd())


def main():

    filename = "Peppers_bit"
    send_image(filename)
    receive_image(filename)

    input("請按 Enter 結束...")

# Data Flow: npy -> .mat ---Channel---> .mat ------> .npy

def receive_image(filename):
    sess.demod_test(QAM_SIZE, nargout=0)

    mat_data = loadmat(f'{filename}_received.mat')

    bit_stream = mat_data['bits_rx']
    bit_stream = bit_stream.flatten()
    np.save(f'../buffer/{filename}_received.npy', bit_stream)

def send_image(filename):
    data = np.load(f'../buffer/{filename}.npy') 
    mat_data = {'bits_tx': data}
    savemat(f'{filename}.mat', mat_data)
    sess.test_one_frame(filename, USE_USRP, QAM_SIZE, nargout=0)


def plot_whole_buffer():
    print("plot_whole_buffer()\n")
    sess.plot_whole_buffer(nargout=0)
    print("end of plot_whole_buffer()\n")


if __name__ == "__main__":
    main()
