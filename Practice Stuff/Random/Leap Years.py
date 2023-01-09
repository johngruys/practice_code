def f(x):
    return x%4

print ("Please input a year below, then press enter.")
x = int(input ())



if (f(x) == 0) and (x<2022):
    print ("The year " + str(x) + " had 366 days")

if (f(x) != 0) and (x<2022):
    print ("The year " + str(x) + " had 365 days")

if (f(x) == 0) and (x>2022):
    print ("The year " + str(x) + " will have 366 days")

if (f(x) != 0) and (x>2022):
    print ("The year " + str(x) + " will have 365 days")

if x == 2022:
    print ("This year is not a leap year.")
    