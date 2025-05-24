import uhd

usrp = uhd.usrp.MultiUSRP("addr=192.168.10.2")
print("Device info:")
print(usrp.get_pp_string())