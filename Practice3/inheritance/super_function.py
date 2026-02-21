class Parent: 
    def __init__(self): print("parent")
class Child(Parent): 
    def __init__(self): super().__init__()
Child()

"""When you create Child(), its constructor runs. 
super().__init__() inside it calls Parent's constructor, so parent is printed"""