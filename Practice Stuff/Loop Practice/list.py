def lec(n, d):
    q = 0
    nextq = q + 1
    while (nextq * d) < n:
        q = nextq
        nextq = q+1
    
    remainder = n - (q * d)
    
    return (q, remainder)

print(lec(12, 2))


    