import math # IMPORTANT

### TODO ###
# Import math in new file
# Add devices as they were in previous file (maintaining motor directions)
# Add distance sensor to devices, mount
# Loosen claw position to be wider
# Compile to see any obvious bugs
# Run through main sequence to check the rest step by step

# Begin project code
# General Parameters + Initialization
shoulder_motor_velocity = 30
forearm_motor_velocity = 15
forearm_motor1.set_velocity(forearm_motor_velocity)
forearm_motor2.set_velocity(forearm_motor_velocity)

# Function to calibrate both limbs of the bot
def calibrate():
    # Calibrate shoulder
    calibrate_shoulder()
    # Calibrate forearm
    calibrate_forearm()
    
# Function to calibrate shoulder joint
def calibrate_shoulder():
    # Calibration Parameters
    shoulder_calibration_velocity = 80
    shoulder_motor.set_velocity(shoulder_calibration_velocity)

    # Start by moving away from limit switch a little in case already pressed
    shoulder_motor.spin(REVERSE)
    wait(2, SECONDS)

    # Move back until switch is pressed 
    while not shoulder_limit.pressing():
        shoulder_motor.spin(FORWARD)
    shoulder_motor.stop()

    # Set motor encoder to current angle (78 degrees * 120 gear ratio)
    shoulder_motor.set_position(9360, DEGREES)

    # Move off limit switch to allow motion (+ better starting position)
    shoulder_motor.spin(REVERSE)
    wait(2, SECONDS)
    shoulder_motor.stop()
    
# Function to calibrate elbow joint
### Run Bicep Calibration First! ###
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

    # Go to starting position (off of limit switch)
    forearm_motor1.spin(FORWARD)
    forearm_motor2.spin(FORWARD)
    wait(1, SECONDS)

    forearm_motor1.stop()
    forearm_motor2.stop()
    
    
# Function that performs forward kinematics to calculate future cartesian coordinates from current forearm value (to check if valid)
# Passed theta1, theta2 in degrees, returns (x, y) in inches
def forward_kinematics(shoulder_angle, forearm_angle):
    # Params
    bicep_length = 10.75
    forearm_length = 11

    # Convert to radians, Calculate x val
    shoulder_radians = math.radians(shoulder_angle)
    forearm_radians = math.radians(forearm_angle)

    shoulder_x = math.cos(shoulder_radians) * bicep_length
    shoulder_y = math.sin(shoulder_radians) * bicep_length

    alpha = 2 * math.pi - shoulder_radians - forearm_radians

    forearm_x = shoulder_x - forearm_length * math.cos(alpha)
    forearm_y = shoulder_y + forearm_length * math.sin(alpha)

    # Resulting position
    return forearm_x, forearm_y
    
    
    
# Wrapper for motors to verify requested angle before moving forearm
def forearm_go_to(angle):
    # Parameters
    min_forearm_angle = 135
    max_forearm_angle = 1135

    # Convert to real angle using gear ratio
    real_angle = angle * 5

    # Verify angle is within operating range
    if (real_angle > max_forearm_angle) or (real_angle < min_forearm_angle):
        print("Requested angle outside of operating range")
        return False

    # Get cartesian coordinates from current shoulder angle and requested theta2
    shoulder_theta = shoulder_motor.position(DEGREES) / 120
    forearm_theta = angle
    
    forearm_x, forearm_y = forward_kinematics(shoulder_theta, forearm_theta)

    ### DEBUGGING
    # print("Requested Coordinates")
    # print(forearm_x, forearm_y)

    # Stop if within an inch of table, but y=0 corresponds to zero in the coordinate 
    # system we made for the kinematics where the origin is the pivot of the shoulder joint
    # so add 2 inches to y to offset
    forearm_y += 2
    if (forearm_y < 1):
        print("Requested angle results in collision")
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

    # Convert to real angle using gear ratio
    real_angle = angle * 120

    # Check within operating range
    if (real_angle < min_shoulder_angle) or (real_angle > max_shoulder_angle):
        print("Requested angle outside of operating range")
        return False

    # Get cartesian coordinates from current forearm angle and requested theta1
    shoulder_theta = angle
    forearm_theta = forearm_motor1.position(DEGREES) / 5

    forearm_x, forearm_y = forward_kinematics(shoulder_theta, forearm_theta)

    ### DEBUGGING
    # print("Requested Coordinates")
    # print(forearm_x, forearm_y)
    
    # Stop if within an inch of table, but y=0 corresponds to zero in the coordinate 
    # system we made for the kinematics where the origin is the pivot of the shoulder joint
    # so add 2 inches to y to offset
    forearm_y += 2
    if (forearm_y < 1):
        print("Requested angle results in collision")
        return False
    else:
        # Angle is good to move to
        shoulder_motor.spin_to_position(real_angle, DEGREES)
        return True
    
# Function to fully open claw
def open_claw():
    claw_servo.set_position(-50)

# Function to close claw (hopefully around can)
def close_claw():
    claw_servo.set_position(50)
    
# Function to dump grabbed can behind robot, destination hardcoded
# Assumes can has been grabbed
def dump_can():
    # Move limbs
    shoulder_go_to(77)
    forearm_go_to(220)
    
    # Drop can
    open_claw()
    
# Function to perform inverse kinematics, given X and Y coordinates (inches)
# Returns 2 values, (Theta1, Theta2) (degrees) which result in the given x, y coordinates
def inverse_kinematics(x, y):
    # Params
    l1 = 10.75 # Bicep
    l2 = 11 # Forearm
    
    # Calculate theta2 first
    numerator = ((l1**2) + (l2**2) - (x**2) - (y**2))
    denominator = 2 * l1 * l2
    theta2 = math.acos(numerator/denominator)
    
    # Calculate theta1 from theta2
    numerator = (l2 * math.sin(theta2))
    denominator = math.sqrt((x**2) + (y**2))
    theta1 = math.atan(y/x) + math.asin(numerator/denominator)
    
    # Convert to degrees and return
    theta1 = math.degrees(theta1)
    theta2 = math.degrees(theta2)
    return theta1, theta2



# Function to return angle values corresponding to the next can based on distance sensor information
def get_angles():
    # Parameters
    delta_x = 5 # Padding for x val
    y = 4 # Adjustable y val of cans
    
    min_distance = 12
    max_distance = 20
    
    ### Distance
    distance = distance_sensor.object_distance(INCHES)
    x = distance + delta_x
    
    ### DEBUGGING ###
    # print("Distance sensor reading:")
    # print(distance)
    # print("x,y for inverse kinematics:")
    # print(x, y)
    
    # Verify x is within range of arm
    if (x < min_distance) or (x > max_distance):
        print("Can outside effective range")
        return None
    
    
    # Perform inverse kinematics
    theta1, theta2 = inverse_kinematics(x, y)
    return theta1, theta2


# Function to drive the can grabbing, assumes calibration prior
# Passed number of cans to grab
def grab_cans(num_cans):
    # Repeat for each can
    for i in range(num_cans):
        # Get angles from kinematics
        theta1, theta2 = get_angles()
        # Move arms to position
        forearm_go_to(theta2)
        shoulder_go_to(theta1)
        # Grab the can
        close_claw()
        wait(1, SECONDS)
        # Dump the can
        dump_can()
        

# Testing #
print("--------------------")

# Calibrate
calibrate()

### Get angles
## Check that the distances make sense, adjust params of get_angles() so X is right
# theta1, theta2 = get_angles()
# print("theta1, theta2 for can:")
# print(theta1, theta2)



### Move Arms
# forearm_go_to(theta2)
# shoulder_go_to(theta1)


### Grab the can + dump
# close_claw()
# wait(1, SECONDS)
# # Dump the can
# dump_can()


### All together now
# grab_cans(3)

# Only 123 lines of actual code, cool


