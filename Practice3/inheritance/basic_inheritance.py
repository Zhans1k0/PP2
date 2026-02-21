class Parent: 
    def hello(self): print("hi")
class Child(Parent): pass
Child().hello()

"""Child is empty. The (Parent) means it takes everything from Parent. 
So Child().hello() works and prints hi"""