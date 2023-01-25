# read data from stickcube arduino and save into a csv file
# data outputted over serial 

# adapted from read_data_v2.py

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
    #print(pieces)
    if len(pieces)==0 or data.find('Time',0,len(data))==-1:
        print('fail')
        return 'fail'
    numbers = []
    for i,piece in enumerate(pieces):
        splitup = piece.split(' ')
        print(splitup)
        numbers.append(try_float(splitup[-1]))
    return numbers

def parse_line(line):
    # parses the line according to the data stardards specified in the readme
    pieces = line.split('\t')
    #print(pieces)

    if len(pieces)==0 or line.find('Time',0,len(line))==-1:
        return 'fail'

    # data from this function is outputted as a list of strings and floats 
    # each string is the type of data corresponding to the float behind it
    data = []
    for i,piece in enumerate(pieces):
        name_val = piece.split(' ')
        print(name_val)
        data.append(name_val[0])
        data.append(name_val[1])

    return data


def get_datatype_ind(name):
    # get the specific index in the data array for whatever data type is specified in 'name'
    if name == 'Time:':
        return 0
    elif name == 'r:':
        return 1
    elif name == 'i:':
        return 2
    elif name == 'j:':
        return 3
    elif name == 'k:':
        return 4
    elif name == 'gyro_reading':
        return 5
    elif name == 'accel_reading':
        return 6
    elif name == 'torques':
        return 7
    elif name == 'wheel_rates':
        return 8
    elif name == 'mag_vec':
        return 9
    elif name == 'body_rates':
        return 10
    elif name == 'xang:':
        return 11
    elif name == 'yang:':
        return 12



def initialize(baud):
    # make sure baud rate below matches that of the arduino
    #ser = serial.Serial('COM7',115200)
    ser = serial.Serial('COM7',baud)
    curr_dir = os.getcwd()

    date_str = datetime.now().strftime("%m-%d-%Y_%H-%M-%S")
    filename = date_str + '.csv'
    full_path = os.path.join(curr_dir, filename)

    ser.flushInput()
    ser.flushOutput()

    cols = ['time', 'r','i','j','k', 'gyro_reading', 'accel_reading', 'torques', 'wheel_rates', 'mag_vec', 'body_rates','x_angle', 'y_angle']

    return [ser,full_path,cols]

def read_continuously(ser):
    # read data until it's given the stopping signal from the arduino
    flag = False;
    all_data = [[-1],[-1],[-1],[-1],[-1],[-1],[-1],[-1],[-1],[-1],[-1],[-1],[-1]]
    #all the different possible types of data that could be outputted by theh arduino
    

    while flag == False:
        data = ser.readline()
        s = codecs.decode(data, 'UTF-8')
        print(s)
        #print('endline')
        #ser.flushInput()
        #ser.flushOutput()
        # if we see the signal to the end the test, stop taking data
        if s.find('end',0,len(s)) != -1:
            flag = True

        data_line = parse_line(s)
        print(data_line)
        print(len(data_line))
        if data_line == 'fail':
            continue
        else:
            for j in range(round(len(data_line)/2)):
                ind = get_datatype_ind(data_line[2*j])
                print(ind)
                print(all_data[ind])
                all_data[ind].append(data_line[2*j+1])


    # fill in empty data slots so the lists are the same size (required for making a numpy array)
    list_length = len(all_data[0])
    for list in all_data:
        if len(list)<list_length:
            for i in range(list_length-len(list)):
                list.append(float('NaN'))

    return all_data


def save_data(all_data, cols, full_path):
    #print(all_data[0])
    print(all_data)
    df = pd.DataFrame(np.array(all_data).T,index=all_data[0],columns=cols)
    df.to_csv(full_path)
    #print(full_path)
    print('DATA SAVED UNDER '+full_path)

def start_test(ser):
    tmax_str = input('Enter the time to save serial data (in seconds): ')
    tmax = float(tmax_str)
    t0 = time.time()
    t = 0
    ser.write(bytes(tmax_str, 'utf-8'))