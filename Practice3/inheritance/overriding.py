class Parent: 
    def show(self): print("parent")
class Child(Parent): 
    def show(self): print("child")
Child().show()

"""Parent has a show() method. Child has the same method but with different text. 
When you call Child().show(), it uses its own version, so child is printed"""