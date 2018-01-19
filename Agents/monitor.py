#!/usr/bin/env python3

from threading import Thread, Event
from time import sleep
from . import misc_utils as misc
from . import exchange as exch

class Monitor (misc.BPA):
	def __init__ (self, params):
		misc.BPA.__init__ (self, None, params)

		self._interval = self._params ['interval']
		if self._interval >= 3600 * 24:
			self._candle = 'day'
		elif self._interval >= 3600:
			self._candle = 'hour'
		elif self._interval >= 1800:
			self._candle = 'thirtyMin'
		elif self._interval >= 300:
			self._candle = 'fiveMin'
		else:
			self._candle = 'oneMin'

		self._market = self._params ['market']
		self._Stop = Event ()
		self._execThread = None

	def start_sim (self):
		resc, ticks = exch.get_candle_ticks (self._market, self._candle, False)
		if not resc:
			self.shout ('Can not get history from exchange, please check')
		else:
			self._Stop.clear ()

			def monitor ():
				while (not self._Stop.is_set ()) and (len(ticks) > 0):
					tick = ticks.pop(0)
					ticker = {'Ask':None,'Bid':None,'Last':tick['C']}   
					data = {**tick, **ticker}

					self.BroadCast (data)
					#self._Stop.wait (0.001)

				self._Stop.set()

			self._execThread = Thread (name = "monitor", target = monitor)
			self._execThread.daemon = True
			self._execThread.start () 

	def start (self):
		resc, ticks = exch.get_candle_ticks (self._market, self._candle, False)
		self._Stop.clear ()
		def monitor ():
			while not self._Stop.is_set ():
				resc, ticks = exch.get_candle_ticks (self._market, self._candle, True)
				rest, ticker = exch.get_ticker (self._market)
				if resc and rest:
					tick = ticks [0]
					data = {**tick, **ticker}

					# broadcast to subcribers
					self.BroadCast (data)
				else:
					self.shout ('Can not get data from exchange for market {mar}, please check'.format (mar = self._market))
				self._Stop.wait (self._interval)
			
			self._Stop.set ()

		self._execThread = Thread (target = monitor)
		self._execThread.daemon = True
		self._execThread.start () 

	def stop (self):
		self._Stop.set ()
		self._execThread.join ()
