security = {}

user = input ("Username: ")

if not user in security.keys():
    print ("Not Registered")

else: 
    password = input("Password")
    if password != security[user]:
        print("Error")
    
    else: 
        print ("Hello ")
