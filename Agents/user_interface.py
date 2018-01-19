#!/usr/bin/env python3

from time import sleep
import curses
from curses import wrapper, doupdate

from threading import Thread, Event 

try:
	from . import console_utils as cls
except (SystemError, ImportError):
	import console_utils as cls

class AWindow(object):
	def __init__(self, h, w, y, x, initial_content = None, bkgd = None, archive_limit = 20, **kwargs):
		self._win = curses.newwin (h, w, y, x)
		
		self._win.scrollok (True)
		self._win.clear ()
		self._win.idlok (True)
		self._archive_limit = archive_limit
		self._archive = []

		#if bkgd is not None:
		#	self.win.bkgd = bkgd

		if initial_content is not None:
			self.addstr (initial_content, **kwargs)

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

	def refresh (self):
		self._win.noutrefresh ()


class UserInterface(cls.ConsoleScreen):
	def __init__ (self, title):
		self.title  = title

		self.tltWin = None
		self.tipWin = None
		self.evaWin = None
		self.curWin = None
		
		self.maxX = None 
		self.maxY = None 


		cls.ConsoleScreen.__init__ (self)

	def start (self):
		cls.ConsoleScreen.start (self)

		self.initConsole ()

		def worker ():
			while (not self._Stop.is_set()):
				resized = curses.is_term_resized(self.maxY, self.maxX)
				if resized:
					self.initConsole (refresh = True)
				doupdate ()
				self._Stop.wait (0.1)

		self._execThread = Thread (name = "curses_ui", target = worker)
		self._execThread.start ()

		self.enabled = True

	def end (self):
		self.enabled = False
		cls.ConsoleScreen.end (self)

	def initConsole (self, refresh = False):
		self.clsLock.acquire ()

		self.maxY, self.maxX = self.screen.getmaxyx ()
		
		curses.start_color ()
		curses.init_pair (1, curses.COLOR_GREEN , curses.COLOR_BLACK)
		curses.init_pair (2, curses.COLOR_RED   , curses.COLOR_BLACK)
		curses.init_pair (3, curses.COLOR_WHITE , curses.COLOR_BLACK)

		self.screen.refresh ()

		if self.maxY < 20 or self.maxX < 40:
			self.screen.clear ()
			self.screen.addstr (0,0, "Screen to small to show in colorful mode!", curses.color_pair(3))
		else:
			self.showSubWindows (refresh)

		self.clsLock.release ()

	def showSubWindows (self, resize):
		self.showTitle      (resize)
		self.showTip        (resize)
		self.showEvaluation (resize)
		self.showCurrent    (resize)

	@staticmethod
	def createWindow (h, w, y, x, title = None, refWin = None, initial_content = None, bkgd = None):
		WinBox = curses.newwin (h, w, y, x)
		WinBox.box ()
		if title is not None:
			WinBox.addstr (0, 2, '[' + title + ']')
		WinBox.noutrefresh ()

		if refWin is None:
			Win = AWindow (h-2, w-2, y+1, x+1, initial_content = initial_content, bkgd = bkgd)
			Win.refresh ()
		else:
			Win = refWin
			Win.win.resize (h-2, w-2)
			Win.win.mvwin  (y+1, x+1)
			Win.restore ()

		return Win 

	def showTitle (self, resize = False):
		if self.tltWin == None or resize:
			h = 2 + 2
			self.tltWin = self.createWindow (h, self.maxX, 0, 0, refWin = self.tltWin if (self.tltWin is not None) and resize else None, bkgd = curses.color_pair (3), initial_content = self.title)
		
	def showTip (self, resize = False):
		if self.tipWin == None or resize:
			h = 4 + 2
			self.tipWin = self.createWindow (h, self.maxX, 4, 0, "Tips", refWin = self.tipWin if (self.tipWin is not None) and resize else None, bkgd = curses.color_pair(3)) 

	def showEvaluation (self, resize = False):
		if self.evaWin == None or resize:
			h = self.maxY - 10 
			w = self.maxX // 2
			self.evaWin = self.createWindow (h, w, 10, 0, "Trading activities", refWin = self.evaWin if (self.evaWin is not None) and resize else None, bkgd = curses.color_pair(3))

	def showCurrent (self, resize = False):
		if self.curWin == None or resize:
			h = self.maxY - 10
			w = self.maxX - (self.maxX // 2)
			self.curWin = self.createWindow (h, w, 10, self.maxX // 2, "Latest info", refWin = self.curWin if (self.curWin is not None) and resize else None, bkgd = curses.color_pair(3))

	def print_on_window (self, window, *args, **kwargs):
		if self.enabled:
			self.clsLock.acquire ()
			window.addstr (*args, **kwargs)
			self.clsLock.release ()
		else:
			#print (args[0])
			pass

	def printEva (self, text, **kwargs):
		if 'good' in kwargs.keys():
			cp = 1 if kwargs['good'] else 2
			self.print_on_window (self.evaWin, text + '\n', curses.color_pair(cp) if self.enabled else None)
		else:
			self.print_on_window (self.evaWin, text + '\n')

	def printTip (self, text, **kwargs):
		self.print_on_window (self.tipWin, text + '\n')

	def printCur (self, text, **kwargs):
		if 'good' in kwargs.keys():
			cp = 1 if kwargs['good'] else 2
			self.print_on_window (self.curWin, text + '\n', curses.color_pair(cp) if self.enabled else None)
		else:
			self.print_on_window (self.curWin, text + '\n')

def main (stdscr):
	ui = UserInterface ("Test")

	print ("Hello")

	ui.start ()

	for i in range(0,10):
		ui.printEva ("111111111111111111111111111111111111111111111111111111111111111111111111111111111111111",good=True)
		sleep (0.5)
		ui.printEva ("222222222222222222222222222222222222222222222222222222222222222222222222222222222222222",good=False)
		sleep (0.5)
		ui.printEva ("111111111111111111111111111111111111111111111111111111111111111111111111111111111111111",good=True)
		sleep (0.5)
		ui.printEva ("222222222222222222222222222222222222222222222222222222222222222222222222222222222222222",good=False)
		sleep (0.5)
		ui.printEva ("111111111111111111111111111111111111111111111111111111111111111111111111111111111111111")
		sleep (0.5)
		ui.printEva ("222222222222222222222222222222222222222222222222222222222222222222222222222222222222222")
		sleep (0.5)

	try:
		while True:
			pass
	except KeyboardInterrupt:
		pass

	ui.end ()

if __name__ == "__main__":
	wrapper (main)
	exit (0)
