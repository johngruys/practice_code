
class Person():
    def __init__(self, name, age):
        self.name = name
        self.age = age
    def __str__(self):
        return f"{self.name}, {self.age}"
    def get_contact(self):
        return f"Hi, my name is {self.name}"

person1 = Person("Bob", 4)
g = input()


print(type(g))
 



