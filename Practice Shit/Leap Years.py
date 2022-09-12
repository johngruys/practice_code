def f(x):
    return x%4

x = int(input ())

if f(x) == 0:
    print ("366 days")

if f(x) != 0:
    print ("365 days")