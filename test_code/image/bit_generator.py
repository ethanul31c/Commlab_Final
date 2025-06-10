import numpy as np
import os

def bit_generator(a, filename):
  a = a/2 + 128
  b = np.unpackbits(a.astype(np.uint8))
  np.save(os.path.join(os.path.dirname(__file__), f'../../buffer/{filename}_bit.npy'), b)

if __name__ == "__main__":
  a = np.load("../../buffer/Peppers_com.npy")
  bit_generator(a, "Peppers"+"_com")
  