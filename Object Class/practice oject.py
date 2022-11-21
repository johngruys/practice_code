class Person():
    def __init__(self, name, age):
        self.name = name
        self.age = age
    def __str__(self):
        return self.name + ", " + str(self.age)
    def get_contact(self):
        return self.name 

person1 = Person("Bob", 954)

print(person1)

