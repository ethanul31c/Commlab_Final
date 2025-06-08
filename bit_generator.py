import numpy as np

def bit_generator(a):
  a = a/2 + 128
  b = np.unpackbits(a.astype(np.uint8))
  np.save('./buffer/Peppers_bit.npy', b)

if __name__ == "__main__":
  a = np.load("./buffer/Peppers_com.npy")
  bit_generator(a)
  