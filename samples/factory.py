import sys
sys.path.append('..')

from inner import inner, class_inner

# Inner factory    
class Product:
    @class_inner
    class Factory:
        param1 : str
        param2 : int
        def __call__(self, param3):
            obj = self.outer()
            obj.param1 = self.param1
            obj.param2 = self.param2
            obj.param3 = param3
            return obj
            
# Outer factory : a it less natural
class Factory:
    param1 : str
    param2 : int
    @inner
    class product:
        def __init__(self, param3):
            self.param3 = param3
        def stuff(self):
            return do_stuff(self.param3, self.outer.param1)


# We can del factory reference after use
class Factory:
    param1 : str
    param2 : int
    @inner
    class product:
        def __init__(self, param3):
            self.param3 = param3
            self.param1 = self.outer.param1
            del self.outer
        def stuff(self): 
            return do_stuff(self.param3, self.param1)

