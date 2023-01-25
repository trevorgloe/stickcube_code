## Script for reading and analyzing data after test
#
# Written for ETOILES lab project Stickcube
# Author: Trevor Loe

import csv
import numpy as np
import matplotlib.pyplot as plt


reader = csv.reader(open("12-07-2021_10-35-17.csv", "rb"), delimiter=",")
data = []
cnt = 1
with open('12-07-2021_10-35-17.csv', newline='') as f:
    reader = csv.reader(f)
    for row in reader:
        print(row)
        floatrow = []
        # ignore the first 2 rows (first row is labels, second row is all -1)
        if cnt > 2:
            for str in row:
                # error handling for when there is not a valid string
                try:
                    floatrow.append(float(str))
                except:
                    floatrow.append(float("NaN"))
            data.append(floatrow)
        cnt = cnt + 1
        print(cnt)

#print(data)
# create numpy array of data
npdata = np.array(data).astype("float")

# plot angles from complementary filter over time
plt.figure()
plt.plot(npdata[:,0],npdata[:,13])
plt.plot(npdata[:,0],npdata[:,12])
plt.legend(['y angle','x angle'])
plt.xlabel('Time [ms]')
plt.ylabel('Angle [deg]')

# plot quaternion components over time
plt.figure()
plt.plot(npdata[:,0],npdata[:,2])
plt.plot(npdata[:,0],npdata[:,3])
plt.plot(npdata[:,0],npdata[:,4])
plt.plot(npdata[:,0],npdata[:,5])
plt.legend(['r','i','j','k'])
plt.xlabel('Time [ms]')
plt.ylabel('Quaternion Components')

plt.show()