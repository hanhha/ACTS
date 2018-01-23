#!/usr/bin/env python3

from time import sleep
import curses
from curses import wrapper

try:
	from . import console_utils as cls
except (SystemError, ImportError):
	import console_utils as cls

class UserInterface(cls.SimpleWinMan):
	def __init__ (self, title, **kwargs):
		self.tltWin = None
		self.tipWin = None
		self.evaWin = None
		self.curWin = None

		cls.SimpleWinMan.__init__ (self, title, **kwargs)

	def generate (self, resize = False):
		self.showTitle      (resize)
		self.showTip        (resize)
		self.showEvaluation (resize)
		self.showCurrent    (resize)

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

	def printEva (self, text, **kwargs):
		if 'good' in kwargs.keys():
			cp = 1 if kwargs['good'] else 2
			self.print_on_window (self.evaWin, text + '\n', curses.color_pair(cp) if self.enabled else None, **kwargs)
		else:
			self.print_on_window (self.evaWin, text + '\n', **kwargs)

	def printTip (self, text, **kwargs):
		self.print_on_window (self.tipWin, text + '\n', **kwargs)

	def printCur (self, text, **kwargs):
		if 'good' in kwargs.keys():
			cp = 1 if kwargs['good'] else 2
			self.print_on_window (self.curWin, text + '\n', curses.color_pair(cp) if self.enabled else None, **kwargs)
		else:
			self.print_on_window (self.curWin, text + '\n', **kwargs)
	
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

	ui.end ()

if __name__ == "__main__":
	wrapper (main)
	exit (0)
