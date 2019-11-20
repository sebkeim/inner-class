import sys
sys.path.append('..')

from inner import inner

# Item and collection 

class UserList(list):
	@inner
	class user:
		def __init__(self, name):
			self.name = name
			self.outer.append(self)



