# File to read data from an arduino serial connection

import serial
import codecs
import numpy as np
import matplotlib.pyplot as plt

ser = serial.Serial('COM7',9600)

f = open('dataFile.txt','a')

plt.figure()
#plt.axis([0, 10, 0, 2])
t = 0
while 1 :
    data = ser.readline()
    s = codecs.decode(data, 'UTF-8')
    f.write(s)
    print(s)
    ser.flushInput()
    ser.flushOutput()
    f.close()
    f = open('dataFile.txt','a')
    if s != '\n' and s != '\r\n':
        plt.scatter(t, int(s))
        plt.pause(1/9600)
    t = t + 0.05

plt.show()