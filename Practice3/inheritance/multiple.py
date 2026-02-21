class A: 
    def say(self): print("A")
class B: 
    def say(self): print("B")
class C(A,B): pass
C().say()

"""C inherits from both A and B. 
Both have a say() method. Python takes the method 
from the first parent listed — A, so it prints A"""