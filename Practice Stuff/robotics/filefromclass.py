import math

# Begin project code
# Params
shoulder_motor_velocity = 30
forearm_motor_velocity = 15
forearm_motor1.set_velocity(forearm_motor_velocity)
forearm_motor2.set_velocity(forearm_motor_velocity)


### Function to calibrate both parts of the bot
def calibrate():
    # Calibrate shoulder
    calibrate_shoulder()

    # Calibrate forearm
    calibrate_forearm()


### Function to calibrate shoulder joint
def calibrate_shoulder():
    # Calibration Parameters
    shoulder_fast_calibration_velocity = 80
    # shoulder_slow_calibration_velocity = 50
    shoulder_motor.set_velocity(shoulder_fast_calibration_velocity)

    # Start by moving away from limit switch a little in case already pressed
    shoulder_motor.spin(REVERSE)
    wait(2, SECONDS)

    # Move back until switch is pressed (initial click)
    while not shoulder_limit.pressing():
        shoulder_motor.spin(FORWARD)

    # Stop motor
    shoulder_motor.stop()

    # Set motor encoder to 0
    shoulder_motor.set_position(9360, DEGREES)

    # Go to a starting position
    shoulder_motor.spin(REVERSE)
    wait(2, SECONDS)
    shoulder_motor.stop()


### Function to calibrate the forearm section of the arm
# Run Bicep Calibration First! #
def calibrate_forearm():
    # Assuming nothing is in way of forearm since bicep is upright
    forearm_calibration_velocity = 10
    forearm_slow_calibration_velocity = 5
    forearm_motor1.set_velocity(forearm_calibration_velocity)
    forearm_motor2.set_velocity(forearm_calibration_velocity)

    # Back off a little in case pressing limit switch
    forearm_motor1.spin(FORWARD)
    forearm_motor2.spin(FORWARD)
    wait(1, SECONDS)

    # Move forward until limit switch is pressed for first click
    while not (forearm_limit.pressing()):
        forearm_motor1.spin(REVERSE)
        forearm_motor2.spin(REVERSE)

    # Back off a little
    forearm_motor1.spin(FORWARD)
    forearm_motor2.spin(FORWARD)
    wait(1, SECONDS)

    # Second click at slower speed to ensure accuracy
    forearm_motor1.set_velocity(forearm_slow_calibration_velocity)
    forearm_motor2.set_velocity(forearm_slow_calibration_velocity)
    while not forearm_limit.pressing():
        forearm_motor1.spin(REVERSE)
        forearm_motor2.spin(REVERSE)

    # Set motor encoder to 0 and update motor velocity
    forearm_motor1.set_position(135, DEGREES)
    forearm_motor1.set_velocity(forearm_calibration_velocity)
    forearm_motor2.set_position(135, DEGREES)
    forearm_motor2.set_velocity(forearm_calibration_velocity)

    # Go to starting position
    forearm_motor1.spin(FORWARD)
    forearm_motor2.spin(FORWARD)
    wait(1, SECONDS)

    forearm_motor1.stop()
    forearm_motor2.stop()


# Wrapper for motors to verify requested angle before moving forearm
def forearm_go_to(angle):
    # Hardcoded parameters
    min_shoulder_angle = 2360
    max_forearm_angle = 1135
    bicep_length = 10.75
    forearm_length = 11

    # Convert to real angle using gear ratio
    real_angle = angle * 5

    # Check limit switches
    if (forearm_limit.pressing()):
        forearm_motor1.stop()
        forearm_motor1.stop()
        return False

    if (real_angle > max_forearm_angle):
        forearm_motor1.stop()
        forearm_motor2.stop()
        return False

    ## Calculate cartesian coordinates from current angle values
    # Get angles
    shoulder_theta = shoulder_motor.position(DEGREES) / 120
    forearm_theta = real_angle / 5
    # print(shoulder_theta, forearm_theta)

    # Convert to radians, Calculate x val
    shoulder_radians = math.radians(shoulder_theta)
    forearm_radians = math.radians(forearm_theta)

    shoulder_x = math.cos(shoulder_radians) * bicep_length
    shoulder_y = math.sin(shoulder_radians) * bicep_length

    alpha = 2 * math.pi - shoulder_radians - forearm_radians

    forearm_x = shoulder_x - forearm_length * math.cos(alpha)
    forearm_y = shoulder_y + forearm_length * math.sin(alpha) + 2

    # Resulting position
    print("Requested Coordinates")
    print(forearm_x, forearm_y)

    # Stop if within an inch of table
    if (forearm_y < 1):
        print("Requested angles outside of operating range...")
        return False
    else:
        forearm_motor1.spin_to_position(real_angle, DEGREES)
        forearm_motor2.spin_to_position(real_angle, DEGREES)
        return True


# Wrapper for motors to verify requested angle before moving shoulder
def shoulder_go_to(angle):
    # Hardcoded parameters
    min_shoulder_angle = 2360
    max_shoulder_angle = 9360
    min_forearm_angle = 135
    max_forearm_angle = 1135
    bicep_length = 10.75
    forearm_length = 11

    # Convert to real angle using gear ratio
    real_angle = angle * 120

    # Check limit switches
    if (shoulder_limit.pressing()):
        shoulder_motor.stop()
        return False

    # Check within operating range
    if (real_angle < min_shoulder_angle) and (real_angle > max_shoulder_angle):
        shoulder_motor.stop()
        return False

    ## Calculate future cartesian coordinates from current forearm value, check if valid
    # Get angles
    shoulder_theta = real_angle / 120
    forearm_theta = forearm_motor1.position(DEGREES) / 5
    # print(shoulder_theta, forearm_theta)

    # Convert to radians, Calculate x val
    shoulder_radians = math.radians(shoulder_theta)
    forearm_radians = math.radians(forearm_theta)

    shoulder_x = math.cos(shoulder_radians) * bicep_length
    shoulder_y = math.sin(shoulder_radians) * bicep_length

    alpha = 2 * math.pi - shoulder_radians - forearm_radians

    forearm_x = shoulder_x - forearm_length * math.cos(alpha)
    forearm_y = shoulder_y + forearm_length * math.sin(alpha) + 2

    # Resulting position
    print("Requested Coordinates")
    print(forearm_x, forearm_y)

    # Stop if within an inch of the table
    if (forearm_y < 1):
        forearm_motor1.stop()
        forearm_motor2.stop()
        shoulder_motor.stop()
        print("Requested angles outside of operating range...")
        return False
    else:
        # Angle is okay, go to it
        shoulder_motor.spin_to_position(real_angle)
        return True


# Function to fully open claw
def open_claw():
    # Consts
    open_pos = -50
    closed_pos = 50
    # Set position
    claw_servo.set_position(open_pos)

# Function to close claw (hopefully around can)
def close_claw():
    # Consts
    open_pos = -50
    closed_pos = 50
    # Set position
    claw_servo.set_position(closed_pos)