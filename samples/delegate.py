import sys
sys.path.append('..')

from inner import inner

# using innner class allow delegation for two objects that call the same methods
#
# usable for sample by a view controller that manage two lists

class Controller:
	@inner
	class table_user_delegate :
		def items(self):
			return self.owner.users_items()
		def selection(self):
			return self.owner.selected_user
	@inner
	class table_product_delegate :
		def items(self):
			return self.owner.products_items()
		def selection(self):
			return self.owner.selected_product