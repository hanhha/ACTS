#!/usr/bin/env python3

from time import sleep
import curses
from curses import wrapper
from collections import OrderedDict

try:
	from . import console_utils as cls
except (SystemError, ImportError):
	import console_utils as cls

ui_sheet = {
	'VLayout': {
		'title'  : (0, 4),
		'tips'   : (0, 6),
		'HLayout': {
			'VLayout'   : {
				'activities': (0, 0),
				'summary'   : (0, 7),
			},
			'current': (0, 0),
		}
	}
}
ui_sheet = OrderedDict (ui_sheet)

ui_win = {
	'tips': {'title':'Tips'},
	'title': {'text': 'Auto Crypto Trading System'},
	'activities': {'title': 'Trading Actitivites'},
	'summary': {'title': 'Summary'},
}

UI = cls.SimpleWinMan (ui_sheet, ui_win)

def main (stdscr):
	UI.start ()

	for i in range(0,10):
		sleep (10)
	#	ui.printEva ("111111111111111111111111111111111111111111111111111111111111111111111111111111111111111",good=True)
	#	sleep (0.5)
	#	ui.printEva ("222222222222222222222222222222222222222222222222222222222222222222222222222222222222222",good=False)
	#	sleep (0.5)
	#	ui.printEva ("111111111111111111111111111111111111111111111111111111111111111111111111111111111111111",good=True)
	#	sleep (0.5)
	#	ui.printEva ("222222222222222222222222222222222222222222222222222222222222222222222222222222222222222",good=False)
	#	sleep (0.5)
	#	ui.printEva ("111111111111111111111111111111111111111111111111111111111111111111111111111111111111111")
	#	sleep (0.5)
	#	ui.printEva ("222222222222222222222222222222222222222222222222222222222222222222222222222222222222222")
	#	sleep (0.5)

	ui.end ()

if __name__ == "__main__":
	wrapper (main)
	exit (0)
