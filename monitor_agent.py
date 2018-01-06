#!/usr/bin/env python3

from threading import Thread, Event
import exchange as exch
import misc_utils as misc

def moni (inpQ, outQ, params, Stop):
	market = params [0]
	interval = params [1]
	while not Stop.is_set():
	if not inpQ.empty():
		tmp = inpQ.get (block = False)
		res, tick = exch.get_candle_ticks (market, interval, True)
		result = (res, tick[0]) if type(tick) is list else (res, tick)
		misc.fill_outQ (outQ, result)
		if res is False:
			print ('Can not get data from exchange\'s server')
		inpQ.task_done ()

class Monitor (misc.BPA):
	def __init__ (self, interval, market):
		misc.BPA.__init__ (self, None, {})

		self._interval = interval
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

		self._market = market
		self._Stop = Event ()
		self._execThread = None

	def start (self):
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
					print ('Can not get data from exchange for market {mar}, please check'.format (mar = self._market))

		self._execThread = Thread (target = monitor)
		self._execThread.daemon = True
		self._execThread.start () 

	def stop (self):
		self._Stop.set ()
		self._execThread.join ()
