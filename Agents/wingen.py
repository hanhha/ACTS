from collections import OrderedDict

class Window(object):
	def __init__ (self):
		self._w = 0
		self._h = 0
		self._x = 0
		self._y = 0

	@property
	def x (self):
		return self._x

	@x.setter
	def x (self, value):
		self._x = value

	@property
	def y (self):
		return self._y

	@y.setter
	def y (self, value):
		self._y = value

	@property
	def w (self):
		return self._w

	@w.setter
	def w (self, value):
		self._w = value

	@property
	def h (self):
		return self._h

	@h.setter
	def h (self, value):
		self._h = value

	def getWin (self):
		return self.y, self.x, self.h, self.w

class Layout(Window):
	def __init__ (self):
		self._tree = list ()
		self._pool = dict ()

	def distribute (self):
		assert "Need to implement", 0

	def create (self, pool, tree_dict):
		self._pool = pool
		for k, v in tree_dict:
					
		

