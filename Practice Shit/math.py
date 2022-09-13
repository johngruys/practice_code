# Interface to find the exponential 
# growth of an investment

import math #duh

# PERT function
def pert(p, r, t):
    return p * math.exp(r*t)

# Have user define the principal
print ("Please input the initial value of investment")
p = int(input ())

# Have user define the interest on the investment
print ("Please input the rate of interest (Where '1' represents 100%)")
r = int(input ())

print (pert(p, r, t))