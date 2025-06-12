import numpy as np
import matplotlib.pyplot as plt

def psnr(img1, img2):
  return 10 * np.log2(255/np.average(np.power(img1-img2, 2))) 

if __name__ == "__main__":
  filename = "Peppers"
  img = plt.imread(f"../../test_image/{filename}.bmp")
  img_recv = plt.imread(f"../../test_image/{filename}_decom.bmp")
  psnr = psnr(img, img_recv)
  print(psnr)