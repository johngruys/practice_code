# Interface to find the exponential 
# growth of an investment

import math #duh

# PERT function
def pert(p, r, t):
    return p * math.exp(r*t)

# Have user define the principal
print ("Please input the initial value of investment")
p = float(input ())

# Have user define the interest on the investment
print ("Please input the rate of interest (Where '1' represents 100%)")
r = float(input ())

# Have user input the time (in years)
print ("Please input the duration of the investment in years")
t = float(input ())

print (pert(p, r, t)) 