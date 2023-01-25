
# File to read data from an arduino serial connection

import serial
import codecs
import numpy as np
import matplotlib.pyplot as plt
import time
import pandas as pd
from datetime import datetime
import os

def try_float(val):
    try:
        num = float(val)
    except ValueError:
        return 'fail'
    return num

def get_num(data):
    #function that takes the string printed by the arduino and returns an array of float that we can actually use
    pieces = data.split('\t')
    if len(pieces)==0 or data.find('Time',0,len(data))==-1:
        return 'fail'
    numbers = []
    for i,piece in enumerate(pieces):
        splitup = piece.split(' ')
        print(splitup)
        numbers.append(try_float(splitup[-1]))
    return numbers


ser = serial.Serial('COM7',115200)
curr_dir = os.getcwd()


while True:

    tmax_str = input('Enter the time to save serial data (in seconds): ')
    tmax = float(tmax_str)
    t0 = time.time()
    t = 0
    
    flag = False;
    date_str = datetime.now().strftime("%m-%d-%Y_%H-%M-%S")
    filename = date_str + '.csv'
    full_path = os.path.join(curr_dir, filename)
    ser.write(bytes(tmax_str, 'utf-8'))
    cols = ['Theta x', 'Theta y']
    #df = pd.DataFrame(np.array([[-1,-1]]),index=['-1'],columns=cols)
    all_data = [[-1],[-1],[-1]]
    ser.flushInput()
    ser.flushOutput()

    while flag == False:
        data = ser.readline()
        s = codecs.decode(data, 'UTF-8')
        print(s)
        #print('endline')
        #ser.flushInput()
        #ser.flushOutput()
        if s.find('waiting',0,len(s)) != -1:
            flag = True

        numtest = get_num(s)
        if numtest == 'fail':
            continue
        else:
            temp = numtest
            print(temp)
            all_data[0].append(t)
            all_data[1].append(numtest[1])
            all_data[2].append(numtest[2])

        t = time.time() - t0

    print(all_data[1:3])
    df = pd.DataFrame(np.array(all_data[1:3]).T,index=all_data[0],columns=cols)
    df.to_csv(full_path)
    print(full_path)
    print('DONE')


plt.show()

