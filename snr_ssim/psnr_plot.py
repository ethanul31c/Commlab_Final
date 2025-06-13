import numpy as np
import matplotlib.pyplot as plt

if __name__ == "__main__":
  
  plt.figure()

  f = np.load("./256_PSNR.npz")
  plt.plot(f['SNR_list'], f['PSNR_list'], marker = '*')
  f = np.load("./64_PSNR.npz")
  plt.plot(f['SNR_list'], f['PSNR_list'], marker = '*')
  f = np.load("./32_PSNR.npz")
  plt.plot(f['SNR_list'], f['PSNR_list'], marker = '*')

  plt.title("PSNR vs SNR in different QAM size (420 compression)")
  plt.xlabel("SNR (dB)")
  plt.ylabel("PSNR (dB)")
  plt.legend(['256QAM', '64QAM', '32QAM'])
  plt.savefig("snr_psnr.png")
  plt.show()