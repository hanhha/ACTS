#!/usr/bin/env python3

from time import sleep
import curses
from curses import wrapper
from collections import OrderedDict

try:
	from . import console_utils as cls
except (SystemError, ImportError):
	import console_utils as cls

ui_sheet = OrderedDict ({
	'VLayout': OrderedDict({
		'title'  : (0, 4),
		'tips'   : (0, 6),
		'HLayout': OrderedDict({
			'VLayout'   : OrderedDict({
				'activities': (0, 0),
				'summary'   : (0, 7),
			}),
			'current': (0, 0),
		})
	})
})

ui_win = {
	'tips': {'title':'Tips'},
	'title': {'text': 'Auto Crypto Trading System'},
	'activities': {'title': 'Trading Actitivites'},
	'summary': {'title': 'Summary'},
	'current': {'title': 'Latest data'},
}

UI = cls.SimpleWinMan (ui_sheet, ui_win)

def printEva (text, **kwargs):
	if 'good' in kwargs:
		cp = 1 if kwargs['good'] else 2
		UI.print_on_window ('activities', text + '\n',  curses.color_pair(cp), **kwargs) 
	else:
		UI.print_on_window ('activities', text + '\n', **kwargs)

def printTip (text, **kwargs):
	UI.print_on_window ('tips', text + '\n', **kwargs)

def printCur (text, **kwargs):
	if 'good' in kwargs:
		cp = 1 if kwargs['good'] else 2
		UI.print_on_window ('current', text + '\n',  curses.color_pair(cp), **kwargs) 
	else:
		UI.print_on_window ('current', text + '\n', **kwargs)

def printSum (key, val):
	if key == 'runtime':
		y = 0
		text = "Ret. candlesticks    : {n}".format (n = val)
	elif key == 'cycle':
		y = 1
		text = "Completed trade      : {n}".format (n = val)
	elif key == 'init':
		y = 2
		text = "Initial cap          : {n}".format (n = val)
	elif key == 'last':
		y = 3
		text = "Last trade gross     : {n}".format (n = val)
	elif key == 'on_going':
		y = 4
		text = "Cap on current trade : {n}".format (n = val)

	UI.println_on_window ('summary', y, 0, text)
	

def main (stdscr):
	UI.start ()

	for i in range(0,10):
		sleep (10)
		printEva ("111111111111111111111111111111111111111111111111111111111111111111111111111111111111111",good=True)
		sleep (0.5)
		printEva ("222222222222222222222222222222222222222222222222222222222222222222222222222222222222222",good=False)
		sleep (0.5)
		printEva ("111111111111111111111111111111111111111111111111111111111111111111111111111111111111111",good=True)
		sleep (0.5)
		printEva ("222222222222222222222222222222222222222222222222222222222222222222222222222222222222222",good=False)
		sleep (0.5)
		printEva ("111111111111111111111111111111111111111111111111111111111111111111111111111111111111111")
		sleep (0.5)
		printEva ("222222222222222222222222222222222222222222222222222222222222222222222222222222222222222")
		sleep (0.5)

	UI.end ()

if __name__ == "__main__":
	wrapper (main)
	exit (0)
