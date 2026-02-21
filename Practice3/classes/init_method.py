class Car:
    def __init__(self, brand):
        self.brand = brand

my_car = Car("Toyota")
print(my_car.brand)

"""__init__ runs automatically when you create an object. 
It sets up the object with initial values. 
Here self.brand = brand saves the brand name"""