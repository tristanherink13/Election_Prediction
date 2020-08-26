class MyClass:
    x = 5
    y = 10

class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age
    
    def get_name(self):
        print('Hello, my name is {}'.format(self.name))

p_object = Person('Ella', 42)

p_object.get_name()