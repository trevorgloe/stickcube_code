## stickcube-Arduino

Arduino/python code for the CPCL project Stickcube

This code has been moved from the original repo upon the project not being associated with CPCL or ETOILES.

### Data formatting standards

Data between the arduino and laptop will formatted as timestamped entries containing some (or all) of the follwing:
- Current attitude (quaternion given as 4 numbers ordered `real i j k`)
- Current attitude (2 angles in deg representing the rotation about the x axis and the y axis)
- Current rate-gryo reading (3 element vector ordered `x y z` in rad/sec)
- Current accelerometer reading (3 element vector ordered `x y z` in m/s^2)
- Commanded torques (2 numbers ordered `x_torque y_torque` in N*m; there is no control in the z-axis)
- Reaction wheel angular rates (2 numbers ordered `x_wheel_rate y_wheel_rate` in rad/sec)
- Magnetic field vector (3 element vector ordered `x y z` in microTesla)
- Stickcube angular rates (3 element vector ordered `x_rate y_rate z_rate` in rad/sec)

All numbers referenced above will be formatted as floating point numbers.

A data entry will be formatted as a single line with `\t` separating each piece of data and the entry ending with `\n`.
Each piece of data in the entry will be in the form `data_name: data`.

### Example
`r: 0.2344 \t i: -0.3331 \t j: 0.0012 \t k: -0.8730 \t accel_reading: -1.3423 -2.345 -6.3452 \t wheel_rates: 0.2332 1.4532 \t body_rates: 0.0123 0.0022 0.0001`

### Shorthand names for data pieces
- Current attitude reading (quaternion):
    - `r`
    - `i`
    - `j`
    - `k`
- Current attitude reading (angles):
    - `xang`
    - `yang`
- Current rate-gyro reading: `gyro_reading`
- Current accelerometer reading: `accel_reading`
- Commanded torques: `torques`
- Reaction wheel angular rates: `wheel_rates`
- Magnetic field vector: `mag_vec`
- Stickcube angular rates: `body_rates`
