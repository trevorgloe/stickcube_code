## Animation-based attitude determination test for stickcube
# Data collection from IMU and real-time complementary filter calculations should be running on the arduino while data is being recorded
# Data is sent from the arduino to this script via a serial connection (COM7 by default)
# To run the test the arduino must be connected to the IMU unit and to the computer running this script via a usb port
#
# To run the test execute the following steps, in order:
#   1. Make necessary connections, ensure arduino is recieving power from USB (LEDs on arduino should light up)
#   2. Run associated arduino script 
#   3. Ensure arduino is in standby state (not recording data yet)
#   4. Run this script
#
# Written for testing of the stickcube project for ETOILES 
#
# Author: Trevor Loe

import read_save_data
import make_animation
import numpy as np
import matplotlib.pyplot as plt

# done to test the animation feature
#make_animation.create_animation(np.array([[1,0,0,0],[np.cos(np.pi/8),0,np.sin(np.pi/8),0],[np.cos(2*np.pi/8),0,np.sin(2*np.pi/8),0],[np.cos(3*np.pi/8),0,np.sin(3*np.pi/8),0],[np.cos(4*np.pi/8),0,np.sin(4*np.pi/8),0],[np.cos(5*np.pi/8),0,np.sin(5*np.pi/8),0],[np.cos(6*np.pi/8),0,np.sin(6*np.pi/8),0],[np.cos(7*np.pi/8),0,np.sin(7*np.pi/8),0],[np.cos(np.pi),0,np.sin(np.pi),0]]))

# intitialize serial connection
[ser,full_path,cols] = read_save_data.initialize(115200)

# initialize the test by sending the arduino the amount of time you want to take data for
read_save_data.start_test(ser)

# read data continuously until given a stopping signal from the arduino (arduino must print 'end' to stop the test)
# arduino data must be formatted according to the guidelines on the readme
all_data = read_save_data.read_continuously(ser)

# save data into a csv in the same folder at this file (name will be given by the current date and time
read_save_data.save_data(all_data,cols,full_path)

# plot angles over time
fig = plt.figure();
plt.plot(np.array(list(map(float,all_data[11]))),label="x angle")
plt.plot(np.array(list(map(float,all_data[12]))),label="y angle")
plt.legend()
plt.title('Angles over time')
plt.xlabel('Angles [deg]')
#plt.show()

# to create the animation, we need an array of all the quats
# in this case, it will be the second inner list of all data (all_data is a list of lists)
all_quats = np.array(make_animation.format_quats(all_data[1:5]))
print(all_quats)
make_animation.create_animation(all_quats[2:-1])


