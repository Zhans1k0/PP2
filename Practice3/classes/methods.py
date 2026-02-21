class Car:
    def __init__(self, brand):
        self.brand = brand
    
    def honk(self):
        print(f"{self.brand} says beep!")

my_car = Car("Toyota")
my_car.honk()

"""Methods are functions inside a class.
honk(self) works on the object and can use its data (self.brand). 
Call it with object.method()"""