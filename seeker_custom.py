#!/usr/bin/env python3

from talib import MA_Type
import ta
import misc_utils as misc
import exchange as exch
import seeker

class Seeker (seeker.BaseSeeker):
	def __init__ (self, source, params):
		seeker.BaseSeeker.__init__ (self, source, params)
		self.pre_ptrend = None
		self._pre_cand_trend = None
		
	def check_goal_achieved (self, price):
		gprice = price * (1 - self._fee)
		return (gprice * self._qty_bought) > (self._investment*(1 + self._goal))  

	def store (self, data):
		self.pre_ptrend = self._pre_cand_trend if 'trend' in self.prediction.keys() else None
		seeker.BaseSeeker.store (self, data)
		
	def predict_trend (self, data):
		# C > EMA3 and C > SMA3: rising
		# C < EMA3 and C < SMA3: falling
		# else = pre_trend
		
		# EMA3 > SMA3: pulling up
		# SMA3 > EMA3: pulling down
		# falling and pulling up > 55% : canyon
		# rising and pulling down > 55% : peak
		ema3 = ta.sMA (self.pdarchieve, 3, 'C', MA_Type.EMA)[self.archieve_len-1]
		sma3 = ta.sMA (self.pdarchieve, 3, 'C', MA_Type.SMA)[self.archieve_len-1]
		c        = data ['C']
		
		d  = (ema3 - sma3) / sma3
		
		if c > ema3 and c > sma3:
			ptrend = 'rising' if d >= -0.55 else 'peak'
			self._pre_cand_trend = 'rising'
		elif c < ema3 and c < sma3:
			ptrend = 'falling' if d <= 0.55 else 'canyon'
			self._pre_cand_trend = 'falling'
		else:
			ptrend =  self.pre_ptrend if self.pre_ptrend is not None else ('rising' if d >= 0 else 'falling')
		
		self.prediction ['trend'] = ptrend
		
		return ptrend

	def predict_profitable (self, data):
		# SD >= goal
		# Desired point:  canyon
		sd = ta.sSD (self.pdarchieve, 6, 'C', MA_Type.SMA)[self.archieve_len-1]
		
		#goal_check =  sd > (self._goal * data['Last'])
		goal_check = True
		profitable = ((self.predict('trend',data) == 'canyon') or (self.predict('trend',data) == 'rising' and self.pre_ptrend == 'falling')) and goal_check
		
		if profitable:
			print ('Predict trend {t} - previous predicted trend {pt}'.format(t = self.predict('trend',data), pt = self.pre_ptrend))
			print ('SD {0:20}'.format(sd))
			print ('Price at goal = ' + str((1 + self._goal) * data['Last']))
			print (data)
			
		return profitable

	def predict_harvestable (self, data):
		# sell at goal
		return self.check_goal_achieved (data['Last'])
