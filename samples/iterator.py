import sys
sys.path.append('..')

from inner import inner

# Iterator as inner class
#       
# inspired from https://www.novixys.com/blog/nested-inner-classes-python/

class Cats:
    @inner
    class __iter__:
        count = 0

        def __iter__(self):
             return self
        def __next__(self):
            i = self.count
            if i >= len(self.outer.cats):
                raise StopIteration
            self.count += 1
            return self.outer.cats[i]
 
    def __init__(self):
        self.cats = []
 
    def add(self, name):
        self.cats.append(name)
        return self
 
a = Cats()
a.add('persian')
a.add('siamese')
 
for x in a:
    print(x)

    
 