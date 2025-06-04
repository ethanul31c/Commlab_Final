import numpy as np

if __name__ == "__main__":
  a = np.load("./buffer/Peppers.npy")
  b = np.unpackbits(a.astype(np.uint8))
  np.save('./buffer/Peppers_bit.npy', b)