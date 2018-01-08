#!/usr/bin/env python3

import misc_utils as misc
import monitor as mon

source = mon.Monitor (60, 'BTC-ADA')
display = misc.BPA (source)

source.start ()
try:
	while True:
		pass
except KeyboardInterrupt:
	print ("User interrupt")
source.stop ()
