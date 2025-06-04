import matlab.engine



sess = matlab.engine.start_matlab()
sess.cd(r'C:\\Users\\Ethan\\Desktop\\USRP\\Final\\Commlab_Final\\test_code')
a = sess.add(5.0, 9.0)
print(type(a))
print(a)