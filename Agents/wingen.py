from collections import OrderedDict

class Window(object):
	def __init__ (self):
		self.type = 'win'
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
	def __init__ (self, pool):
		Window.__init__ (self)
		self.type = 'lay'

		self._tree      = list ()
		self._pool      = pool

		self._n_layouts    = 0
		self._fixed_l      = 0
		self.remaining     = 0
		self.remaining_lay = 0

	def distribute (self):
		if self.remaining <= 0:
			raise ValueError ("Not enough room")
		else:
			for idx, o in enumerate (self._tree):
				self.update_child (self._tree[idx-1] if idx > 0 else None, o)		
				if o.type == 'lay':
					o.reset ()	
					i.distribute ()

	def create (self, tree_dict):
		for k, v in tree_dict:
			if k == "HLayout" or k == "VLayout":
				lay = None
				if k == "HLayout":
					lay = HLayout (self._pool)
				else:
					lay = VLayout (self._pool)

				self._tree.append(lay)
				self._n_layouts += 1
				self._tree [-1].create (v)
			else:
				win = Window ()
				win.w, win.h = v
				self._pool [k] = win
				self._tree.append(win)
				self._fixed_l += self.get_var_dim (win)

	def update (self, w, h):
		self.w, self.h = w, h
		self.remaining_lay = self._n_layouts

	def update_child (self, pre_child_win, child_win):
		assert "Need to implement", 0

	def get_var_dim(self, win):
		assert "Need to implement", 0

class HLayout(Layout):
	def get_var_dim(self, win):
		return win.w

	def update (self, w, h):
		Layout.update (self, w, h)
		self.remaining = self.w - self._fixed_l

	def update_child (self, pre_child_win, child_win):
		ch = self.h
		cy = self.y 
		if pre_child_win is None:
			cx = self.x
			cw = child_win.w if child_win.type == 'win' else self.remaining // self._n_layouts
		else:
			cx = pre_child_win.x + pre_child_win.w
			cw = child_win.w if child_win.type == 'win' else self.remaining - 
			
		
class VLayout(Layout):
	def get_var_dim (self, win):
		return win.h

	def distribute (self):
		pass

