import numpy as np
import matplotlib.pyplot as plt

if __name__ == "__main__":
  qam_list = np.array([4, 8, 16, 32, 64, 256])
  ssim_list = np.zeros(qam_list.shape)
  plt.figure()
  
  f = np.load("./4.npz")
  ssim_list[0] = f['SSIM_list'][0]
  f = np.load("./8.npz")
  ssim_list[1] = f['SSIM_list'][0]
  f = np.load("./16.npz")
  ssim_list[2] = f['SSIM_list'][0]
  f = np.load("./32.npz")
  ssim_list[3] = f['SSIM_list'][0]
  f = np.load("./64.npz")
  ssim_list[4] = f['SSIM_list'][0]
  f = np.load("./256.npz")
  ssim_list[5] = f['SSIM_list'][0]
   

  plt.semilogx(qam_list, ssim_list, marker = '*')
  plt.title("SSIM vs QAM size in very noisy channel (amp = 0.01)")
  plt.xlabel("QAM size")
  plt.ylabel("SSIM")
  plt.savefig("snr_ssim_noisy.png")
  plt.show()
