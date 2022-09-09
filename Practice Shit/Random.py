# Function to find the loudness
# in dB of fizz in a soda lol

def f(x):
    import math
    return (4 * math.log((x / 10**-5), 12))

print (f(4))

print (f(10**-3))



