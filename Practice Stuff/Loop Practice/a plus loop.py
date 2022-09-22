list = []

for num in range(0, 21):
    list = list + [num]
    

a = 0 
output = 0
while a < 10:
    for value in list:
        output = output + value
        
        a = a + 1

print (output) 