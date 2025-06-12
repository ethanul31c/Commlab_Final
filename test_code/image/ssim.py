import numpy as np
import matplotlib.pyplot as plt

def ssim(img1, img2):
  L = img1.shape[0]
  W = img1.shape[1]
  mx = np.average(img1)
  my = np.average(img2)
  varx = np.linalg.norm(img1)**2/(L*W*3) - mx**2
  vary = np.linalg.norm(img1)**2/(L*W*3) - my**2
  varxy = np.average(np.multiply(img1-mx, img2-my))
  R = 255
  ssim = (2*mx*my+R)*(2*varxy+R) / ((mx**2+my**2+R)*(varx+vary+R))
  return ssim
if __name__ == "__main__":
  filename = "Peppers"
  img = plt.imread(f"../../test_image/{filename}.bmp")
  img_recv = plt.imread(f"../../test_image/{filename}_decom.bmp")
  ssim = ssim(img, img_recv)
  print(ssim)