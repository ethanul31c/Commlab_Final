import matlab.engine
from scipy.io import savemat
from scipy.io import loadmat
import numpy as np
import sys
import os
import matplotlib.pyplot as plt
sys.path.append("./image")
from image import c420, c420_decom, c422, c422_decom, bit_generator, image_generator, psnr, ssim
from PIL import Image

USE_USRP = 1
QAM_SIZE = 16
ANTENNA_MODE = 2
AMP_HEADER = 0.1
AMP_DATA = 0.1
COMPRESSION = "c420"

try:
    sess = matlab.engine.start_matlab("")
    print("MATLAB 啟動成功！")
except Exception as e:
    print("MATLAB 啟動失敗：", str(e))
    sys.exit(1)  # 非 0 表示異常退出，程式會停止在這裡

sess.cd(os.getcwd())

# 0.01 0.025 0.05 0.1
# AMP_DATA = np.array([0.01, 0.025, 0.05, 0.1])
AMP_DATA = np.array([0.025])
def main():
    SNR_list = np.zeros(AMP_DATA.shape)
    SSIM_list = np.zeros(AMP_DATA.shape)
    PSNR_list = np.zeros(AMP_DATA.shape)
    filename = "Peppers"
    raw_img = plt.imread(f"../test_image/{filename}.bmp")
    plt.imshow(raw_img)
    plt.show()
    if COMPRESSION == "c420":
        c420.c420(raw_img, filename)
    elif COMPRESSION == "c422":
        c422.c422(raw_img, filename)

    com_img = np.load(f"../buffer/{filename}_com.npy")
    bit_generator.bit_generator(com_img, filename)
    for i in range(AMP_DATA.size):
        send_image(filename, AMP_DATA[i])
        SNR_list[i] = receive_image(filename)
        bit_img_recv = np.load(f"../buffer/{filename}_bit_received.npy")
        image_generator.image_generator(bit_img_recv, com_img.shape, filename)
        com_img_recv = np.load(f"../buffer/{filename}_com_received.npy")
        
        if COMPRESSION == "c420":
            c420_decom.c420_decom(com_img_recv, filename)
        elif COMPRESSION == "c422":
            c422_decom.c422_decom(com_img_recv, filename)

        recv_img = plt.imread(f"../test_image/{filename}_decom.bmp") #change here
        plt.imshow(recv_img)
        plt.show()
        # SSIM_list[i] = ssim.ssim(raw_img, recv_img)
        PSNR_list[i] = psnr.psnr(raw_img, recv_img)
    print(SNR_list)
    # print(SSIM_list)
    print(PSNR_list)
    # np.savez(f"../snr_ssim/{QAM_SIZE}.npz", SNR_list = SNR_list, SSIM_list = SSIM_list) #change here
    np.savez(f"../snr_ssim/{QAM_SIZE}_PSNR.npz", SNR_list = SNR_list, PSNR_list = PSNR_list) #change here
    # plt.figure()
    # plt.plot(SNR_list, SSIM_list, marker = '*')
    # plt.title("SSIM vs SNR")
    # plt.xlabel("SNR (db)")
    # plt.ylabel("SSIM")
    # plt.show()
    input("請按 Enter 結束...")

# Data Flow: npy -> .mat ---Channel---> .mat ------> .npy

def receive_image(filename):
    SNR_dB = sess.demod_test(filename, QAM_SIZE)
    mat_data = loadmat(f'{filename}_received.mat')

    bit_stream = mat_data['bits_rx']
    bit_stream = bit_stream.flatten()
    np.save(f'../buffer/{filename}_bit_received.npy', bit_stream)
    return SNR_dB

def send_image(filename, AMP_DATA):
    data = np.load(f'../buffer/{filename}_bit.npy')
    mat_data = {'bits_tx': data}
    savemat(f'{filename}.mat', mat_data)
    sess.test_one_frame(filename, USE_USRP, QAM_SIZE, ANTENNA_MODE, AMP_DATA, AMP_HEADER, nargout=0)


def plot_whole_buffer():
    print("plot_whole_buffer()\n")
    sess.plot_whole_buffer(nargout=0)
    print("end of plot_whole_buffer()\n")


if __name__ == "__main__":
    main()
