import numpy as np

def image_generator(a, shape):
  b = np.packbits(a)
  b = np.reshape(b, shape)
  b = b.astype(np.float32)
  b = (b - 128) * 2
  np.save('./buffer/Peppers_com_recv.npy', b)

if __name__ == "__main__":
  a = np.load("./buffer/Peppers_bit.npy") # should be Peppers_bit_recv
  temp = np.load("./buffer/Peppers_com.npy")
  image_generator(a, temp.shape)
  