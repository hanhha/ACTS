import term

def clearscreen ():
	term.clear ()

def pprint (s, pos = None):
	if pos == 'home':
		term.homePos ()
	elif type (pos) == tuple:
		term.pos (pos[0], pos[1])

	term.writeLine (s)
