# Script to test complementary filter with stored data
import numpy as np


#import test data
moving_accel = np.load('IMU_testdata/moving_accel_data_025dt.npy')
moving_mag = np.load('IMU_testdata/moving_mag_data_025dt.npy')
moving_gyro = np.load('IMU_testdata/moving_rate_data_025dt.npy')

[steps,temp] = moving_accel.shape

for i in range(steps):
    accel_vec = moving_accel[i,:]
    mag_vec = moving_mag[i,:]
    gyro_vec = moving_gyro[i,:]
    print('accelerometer: ')
    print(accel_vec)
    print('magnetometer:')
    print(mag_vec)
    print('gyroscope:')
    print(gyro_vec)

