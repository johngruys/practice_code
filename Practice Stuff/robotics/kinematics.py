import math

# distance_sensor = HIHI
 



## Calculate future cartesian coordinates from current forearm value, check if valid
def get_xy(shoulder_angle, forearm_angle):
    # Params
    bicep_length = 10.75
    forearm_length = 11
    
    # Get angles
    shoulder_theta = shoulder_angle
    forearm_theta = forearm_angle

    # Convert to radians, Calculate x val
    shoulder_radians = math.radians(shoulder_theta)
    forearm_radians = math.radians(forearm_theta)

    shoulder_x = math.cos(shoulder_radians) * bicep_length
    shoulder_y = math.sin(shoulder_radians) * bicep_length

    alpha = 2 * math.pi - shoulder_radians - forearm_radians

    forearm_x = shoulder_x - forearm_length * math.cos(alpha)
    forearm_y = shoulder_y + forearm_length * math.sin(alpha)

    # Resulting position
    return forearm_x, forearm_y
    
    
    
    
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

# Function to dump grabbed can behind robot, destination hardcoded
# Assumes can has been grabbed
def dump_can():
    # Move limbs
    shoulder_go_to(77)
    forearm_go_to(220)
    
    # Drop can
    open_claw()


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
    
    # Debugging
    # print("Distance to can:")
    # print(distance)
    # print("x, y for inverse kinematics:")
    # print(x, y)
    
    # Verify x is within range of arm
    if (x < min_distance) or (x > max_distance):
        print("Can outside effective range")
        return None
    
    
    # Perform inverse kinematics
    theta1, theta2 = inverse_kinematics(x, y)
    return theta1, theta2
    
    
# Function to drive the can grabbing, assumes calibration prior
# Passed number of cans to grab, no return val
def grab_cans(num_cans):
    # Repeat for each can
    for i in range(num_cans):
        # Get angles from kinematics
        theta1, theta2 = get_angles
        # Move arms to position
        forearm_go_to(theta2)
        shoulder_go_to(theta1)
        # Grab the can
        close_claw()
        # Dump the can
        dump_can()
    
    
    



if __name__ == "__main__":

    # Desired point
    x = 21
    y = 4

    # kinematics says
    theta1, theta2 = inverse_kinematics(x, y)
    print(f"Kinematics says: {theta1, theta2}")

    # And foreward kinematics says
    resulting_x, resulting_y = get_xy(theta1, theta2)
    print(f"And get_xy gives: {resulting_x, resulting_y}")







