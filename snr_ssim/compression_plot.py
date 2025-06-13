import numpy as np
import matplotlib.pyplot as plt

if __name__ == "__main__":

  plt.figure()

  f = np.load("./256.npz")
  plt.plot(f['SNR_list'], f['SSIM_list'], marker = '*')
  f = np.load("./256_422.npz")
  plt.plot(f['SNR_list'], f['SSIM_list'], marker = '*')
  f = np.load("./64.npz")
  plt.plot(f['SNR_list'], f['SSIM_list'], marker = '*')
  f = np.load("./64_422.npz")
  plt.plot(f['SNR_list'], f['SSIM_list'], marker = '*')

  plt.title("SSIM vs SNR in different QAM size and compression methods")
  plt.xlabel("SNR (dB)")
  plt.ylabel("SSIM")
  plt.legend(['256QAM, 420', '256QAM, 422', '64QAM, 420', '64QAM, 422'])
  plt.savefig("snr_ssim_com.png")
  plt.show()