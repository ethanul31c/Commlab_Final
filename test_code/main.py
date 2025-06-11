import matlab.engine
from scipy.io import savemat
from scipy.io import loadmat
import numpy as np
import sys
import os
import matplotlib.pyplot as plt
sys.path.append("./image")
from image import c420, c420_decom, bit_generator, image_generator
from PIL import Image

USE_USRP = 1
QAM_SIZE = 256
ANTENNA_MODE = 2
AMP_HEADER = 0.1
AMP_DATA = 0.1

try:
    sess = matlab.engine.start_matlab("")
    print("MATLAB 啟動成功！")
except Exception as e:
    print("MATLAB 啟動失敗：", str(e))
    sys.exit(1)  # 非 0 表示異常退出，程式會停止在這裡

sess.cd(os.getcwd())


def main():

    filename = "Peppers"
    raw_img = plt.imread(f"../test_image/{filename}.bmp")
    plt.imshow(raw_img)
    plt.show()
    c420.c420(raw_img, filename)
    com_img = np.load(f"../buffer/{filename}_com.npy")
    bit_generator.bit_generator(com_img, filename)
    send_image(filename)
    receive_image(filename)
    bit_img_recv = np.load(f"../buffer/{filename}_bit_received.npy")
    image_generator.image_generator(bit_img_recv, com_img.shape, filename)
    com_img_recv = np.load(f"../buffer/{filename}_com_received.npy")
    c420_decom.c420_decom(com_img_recv, filename)

    recv_img = plt.imread(f"../test_image/{filename}_decom.bmp")
    plt.imshow(recv_img)
    plt.show()

    input("請按 Enter 結束...")

# Data Flow: npy -> .mat ---Channel---> .mat ------> .npy

def receive_image(filename):
    sess.demod_test(filename, QAM_SIZE, nargout=0)

    mat_data = loadmat(f'{filename}_received.mat')

    bit_stream = mat_data['bits_rx']
    bit_stream = bit_stream.flatten()
    np.save(f'../buffer/{filename}_bit_received.npy', bit_stream)

def send_image(filename):
    data = np.load(f'../buffer/{filename}_bit.npy') #should be bit 
    mat_data = {'bits_tx': data}
    savemat(f'{filename}.mat', mat_data)
    sess.test_one_frame(filename, USE_USRP, QAM_SIZE, ANTENNA_MODE, AMP_DATA, AMP_HEADER, nargout=0)


def plot_whole_buffer():
    print("plot_whole_buffer()\n")
    sess.plot_whole_buffer(nargout=0)
    print("end of plot_whole_buffer()\n")


if __name__ == "__main__":
    main()
