import curses
from threading import Lock, Event 

class ConsoleScreen(object):
	def __init__ (self):
		self.screen = None
		self.clsLock = Lock ()
		self._execThread = None
		self._Stop = Event ()
		self.enabled = False

	def __del__ (self):
		if self.screen is not None:
			self.end ()

	def start (self):
		self.screen = curses.initscr ()
		curses.noecho ()
		curses.cbreak ()
		self.screen.keypad (True)
		self._Stop.clear ()

	def end (self):
		if self.enabled:
			self._Stop.set ()
			self.enabled = False
			if self._execThread is not None:
				self._execThread.join ()

		self.screen.keypad (False)
		curses.nocbreak ()
		curses.echo ()
		curses.endwin ()

class AWindow(object):
	def __init__(self, h, w, y, x, initial_content = None, bkgd = None, archive_limit = 20, **kwargs):
		self._archive_limit = archive_limit
		self._archive       = []
		self._bkgd          = bkgd

		self.create (h, w, y, x, bkgd)

		if initial_content is not None:
			self.addstr (initial_content, **kwargs)

	def create (self, h, w, y, x, bkgd):
		self._win = curses.newwin (h, w, y, x)

		self._win.scrollok (True)
		self._win.clear ()
		self._win.idlok (True)

		self.refresh ()

		if bkgd is not None:
			self.win.bkgd(bkgd)

		self.refresh ()

	@property
	def win (self):
		return self._win

	def addstr (self, *args, **kwargs):
		self._win.addstr (*args, **kwargs)
		self.refresh ()
		self._archive.append ((args, kwargs))
		if len(self._archive) > self._archive_limit:
			del self._archive [0]

	def restore (self):
		self._win.clear ()
		for archive in self._archive:
			self._win.addstr (*archive[0], **archive[1])
			self.refresh ()

		self.refresh ()

	def refresh (self):
		self._win.noutrefresh ()

	def resize (self, h, w, y, x):
		self.create (h, w, y, x, self._bkgd)
		self.restore ()

class ABoxWindow(AWindow):
	def __init__(self, h, w, y, x, title = None, initial_content = None, bkgd = None, archive_limit = 20, **kwargs):
		self._title = title

		self.createBox (h, w, y, x, title = title)

		AWindow.__init__ (self, h-2, w-2, y+1, x+1, initial_content = initial_content, bkgd = bkgd, archive_limit = archive_limit, **kwargs)

	def createBox (self, h, w, y, x, title = None):		
		self._WinBox = curses.newwin (h, w, y, x)
		self._WinBox.box ()
		if title is not None:
			self._WinBox.addstr (0, 2, '[' + title + ']')
		self._WinBox.noutrefresh ()

	def resize (self, h, w, y, x):
		self.createBox (h, w, y, x, title = self._title)
		AWindow.resize (self, h - 2, w - 2, y + 1, x + 1)
