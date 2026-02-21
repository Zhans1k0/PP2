class Car:
    wheels = 4  # Class variable
    
    def __init__(self, brand):
        self.brand = brand  # Instance variable

car1 = Car("Toyota")
car2 = Car("Honda")
print(car1.wheels)
print(car2.wheels)
print(Car.wheels)

"""wheels is a class variable — shared by all 
objects. self.brand is an instance variable — each object has its own. 
Class variables belong to the class itself, not to each object"""