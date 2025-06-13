import numpy as np
import matplotlib.pyplot as plt

if __name__ == "__main__":
  
  plt.figure()

  f = np.load("./256.npz")
  plt.plot(f['SNR_list'], f['SSIM_list'], marker = '*')
  f = np.load("./64.npz")
  plt.plot(f['SNR_list'], f['SSIM_list'], marker = '*')
  f = np.load("./32.npz")
  plt.plot(f['SNR_list'], f['SSIM_list'], marker = '*')
  f = np.load("./16.npz")
  plt.plot(f['SNR_list'], f['SSIM_list'], marker = '*')
  f = np.load("./8.npz")
  plt.plot(f['SNR_list'], f['SSIM_list'], marker = '*')
  f = np.load("./4.npz")
  plt.plot(f['SNR_list'], f['SSIM_list'], marker = '*')
  
  plt.title("SSIM vs SNR in different QAM size")
  plt.xlabel("SNR (dB)")
  plt.ylabel("SSIM")
  plt.legend(['256QAM', '64QAM', '32QAM', '16QAM', '8QAM', '4QAM'])
  plt.savefig("snr_ssim.png")
  plt.show()
