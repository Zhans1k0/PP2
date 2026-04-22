import math
import random

print(min(3, 7, 1))
print(max(3, 7, 1))
print(abs(-10))
print(round(3.6))
print(pow(2, 3))

print(math.sqrt(16))
print(math.ceil(4.2))
print(math.floor(4.8))
print(math.pi)
print(math.e)

numbers = [1, 2, 3, 4, 5]

print(random.random())
print(random.randint(1, 10))
print(random.choice(numbers))

random.shuffle(numbers)
print(numbers)