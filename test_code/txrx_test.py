import uhd
import numpy as np
import time
import matplotlib.pyplot as plt

usrp = uhd.usrp.MultiUSRP("addr=192.168.10.2")

# 基本參數
rate = 1e6
freq = 100e6
tx_gain = 30
rx_gain = 35
nsamps = 1024
nframes = 10

usrp.set_rx_rate(rate)
usrp.set_tx_rate(rate)
usrp.set_rx_freq(freq)
usrp.set_tx_freq(freq)
usrp.set_rx_gain(rx_gain)
usrp.set_tx_gain(tx_gain)
usrp.set_rx_antenna("RX2")
usrp.set_tx_antenna("TX/RX")

# TX 波形：1kHz 複數正弦波
t = np.arange(nsamps) / rate
tx_waveform = 0.3 * np.exp(2j * np.pi * 1e3 * t).astype(np.complex64)

# 建立 Streamers
st_args = uhd.usrp.StreamArgs("fc32", "sc16")
tx_stream = usrp.get_tx_stream(st_args)
rx_stream = usrp.get_rx_stream(st_args)

tx_md = uhd.types.TXMetadata()
rx_md = uhd.types.RXMetadata()

# 同步起始時間
usrp.set_time_now(uhd.types.TimeSpec(0.0))
time.sleep(0.1)

# 啟動 RX
print("Start RX...")
rx_stream.issue_stream_cmd(uhd.types.StreamCMD(uhd.types.StreamMode.start_cont))
time.sleep(0.05)

# 啟動 TX（持續 1 秒發送）
print("Start TX...")
tx_md.start_of_burst = True
tx_md.end_of_burst = False
start = time.time()
while time.time() - start < 1.0:
    tx_stream.send(tx_waveform, tx_md)
    tx_md.start_of_burst = False
# TX 結尾
tx_md.end_of_burst = True
tx_stream.send(np.zeros_like(tx_waveform), tx_md)

# RX 收多幀
rx_buffer = np.zeros(nsamps * nframes, dtype=np.complex64)
print("Receiving frames...")
for i in range(nframes):
    offset = i * nsamps
    rx_stream.recv(rx_buffer[offset:offset+nsamps], rx_md, timeout=1.0)

# 停止 RX
rx_stream.issue_stream_cmd(uhd.types.StreamCMD(uhd.types.StreamMode.stop_cont))

# 顯示樣本
print("First 10 samples:\n", rx_buffer[:10])
print("Middle 10 samples:\n", rx_buffer[nsamps * (nframes//2):(nsamps * (nframes//2)) + 10])
print("Last 10 samples:\n", rx_buffer[-10:])

# 畫波形
plt.figure()
plt.plot(rx_buffer.real[:200], label="I")
plt.plot(rx_buffer.imag[:200], label="Q")
plt.title("RX I/Q Samples (前 200)")
plt.legend()
plt.grid()

# 畫頻譜
plt.figure()
spectrum = np.fft.fftshift(np.fft.fft(rx_buffer))
freq_axis = np.fft.fftshift(np.fft.fftfreq(len(rx_buffer), 1/rate))
plt.plot(freq_axis / 1e3, 20 * np.log10(np.abs(spectrum) + 1e-12))
plt.title("Spectrum (dB)")
plt.xlabel("Frequency (kHz)")
plt.ylabel("Magnitude (dB)")
plt.grid()

plt.show()
