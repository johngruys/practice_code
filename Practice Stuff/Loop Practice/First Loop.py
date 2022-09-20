tuple = {1, 2, 3, 4, 5, 6, 7, 8, 9}

def f(x):
    return x ** 2
    
def g(x):
    return x / 2
    
for num in tuple:
    if (num%2) == 0:
       print (f(num))
    elif (num%2) != 0:
        print (g(num))
