import numpy as np
import matplotlib.pyplot as plt

if __name__ == "__main__":
  
  plt.figure()
  f = np.load("./256.npz")
  plt.plot(f['SNR_list'], f['SSIM_list'], marker = '*')
  
  plt.title("SSIM vs SNR")
  plt.xlabel("SNR (db)")
  plt.ylabel("SSIM")
  plt.savefig("snr_ssim.png")
  plt.show()
