# function to divide by 100
def c(x):
    return x%100

# function to divide by 4
def f(x):
    return x%4

def test(x):
    if c(x) == 0:
        return "is not a leap year"
    elif f(x) == 0:
        return "is a leap year"
    else:
        return "is not a leap year"

print("Please input year below")
x = int(input ())

print (test(x))
