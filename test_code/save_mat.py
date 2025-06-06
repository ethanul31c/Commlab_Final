import numpy as np
from scipy.io import savemat

data = np.load('../buffer/Peppers_bit.npy')  # 假設檔名為 bitstream.npy

# 將資料以 dict 的形式包裝起來（MATLAB 中需有變數名稱）
mat_data = {'bits_tx': data}

# 儲存成 .mat 檔案
savemat('Peppers_bit.mat', mat_data)