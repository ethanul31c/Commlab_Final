import uhd

usrp = uhd.usrp.MultiUSRP("addr=192.168.10.2")
print("Connected to USRP:", usrp.get_mboard_name(0))

# 設定頻率與增益（可根據你的裝置修改）
usrp.set_rx_rate(1e6)
usrp.set_rx_freq(100e6)
usrp.set_rx_gain(20)

print("RX Rate:", usrp.get_rx_rate())
print("RX Freq:", usrp.get_rx_freq())
print("RX Gain:", usrp.get_rx_gain())
