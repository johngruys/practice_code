# def fac(x):
#     if (x == 1):
#         return 1
#     else: 
#         return x * fac(x-1)


def fac(x):
    numbers = []
    for num in range(x):
        numbers += [num+1]

    product = 1
    for factor in numbers:
        product = product * factor

    return product

print (fac(99999))
