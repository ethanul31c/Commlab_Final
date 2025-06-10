import numpy as np
import os

def image_generator(a, shape, filename):
  b = np.packbits(a)
  size = shape[0]*shape[1]*shape[2]
  b = b[range(size)]
  b = np.reshape(b, shape)
  b = b.astype(np.float32)
  b = (b - 128) * 2
  np.save(os.path.join(os.path.dirname(__file__), f'../../buffer/{filename}_com_received.npy'), b)

if __name__ == "__main__":
  a = np.load("../../buffer/Peppers_bit.npy") # should be Peppers_bit_recv
  temp = np.load("../../buffer/Peppers_com.npy")
  image_generator(a, temp.shape, "Peppers")
  