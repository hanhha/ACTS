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
		self.clsLock.acquire ()
		self._Stop.set ()
		self.clsLock.release ()

		self.screen.keypad (False)
		curses.nocbreak ()
		curses.echo ()
		curses.endwin ()


