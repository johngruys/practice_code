# def fac(x):
#     if (x == 1):
#         return 1
#     else: 
#         return x * fac(x-1)


def fac(x):
    product = 1
    for num in range(x):
        product = product * (num + 1)

    return product

print (fac(99999))
