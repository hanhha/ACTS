#!/usr/bin/env python3

from talib import MA_Type
from Agents import ta
from Agents import misc_utils as misc
from Agents import exchange as exch
from Agents import seeker

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
	
	def previous_optima (self, optima = 'canyon', price = 'C', prev_idx = 0, pcmp = 'gtoe', pivot = 0):
		if (optima in ['canyon', 'peak', 'rising', 'falling']):
			start_idx = prev_idx
			findout   = False
			idx = None
			while (not findout) and ((self.archieve_len - start_idx) > 2):
				i0 = self.archieve_len - start_idx
				i1 = self.archieve_len - i0 - 1
				i2 = self.archieve_len - i1 - 1
				if optima == 'canyon':
					if self.archieve[i2][price] > self.archieve[i1][price] < self.archieve[i0][price]
						findout = True
						idx     = i1
				elif optima == 'peak':
					if self.archieve[i2][price] < self.archieve[i1][price] > self.archieve[i0][price]
						findout = True
						idx     = i1
				elif optima == 'rising':
					if self.archieve[i2][price] < self.archieve[i1][price] < self.archieve[i0][price]
						findout = True
						idx     = i1
				elif optima == 'falling':
					if self.archieve[i2][price] > self.archieve[i1][price] > self.archieve[i0][price]
						findout = True
						idx     = i1
				if findout:
					if pcmp == 'gtoe' and self.archieve[idx][price] >= pivot:
						findout = True
					elif pcm == 'gt' and self.archieve[idx][price] > pivot:
						findout = True
					elif pcm == 'ltoe' and self.archieve[idx][price] <= pivot:
						findout = True
					elif pcm == 'lt' and self.archieve[idx][price] < pivot:
						findout = True
					elif pcm == 'e' and self.archieve[idx][price] == pivot:
						findout = True
					else:
						findout = False
				start_idx -= 1
			return idx, self.archieve[idx][price] if findout else None, None
		else:
			return None, None

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
		
		d  = ema3 - sma3
		
		if self.pre_ptrend == 'rising':
			if c > ema3 and c > sma3:
				ptrend = 'rising'
			elif self.previous_optima ('peak', 'C', 1, data['C'])
		#	self._pre_cand_trend = 'rising'
		#elif c < ema3 and c < sma3:
		#	ptrend = 'falling' if d <= 0.55 else 'canyon'
		#	self._pre_cand_trend = 'falling'
		#else:
		#	ptrend =  self.pre_ptrend if self.pre_ptrend is not None else ('rising' if d >= 0 else 'falling')
		if data['C'] >= self.archieve [self.archieve_len-1]['C']:
			i0, p0 = self.previous_optima ('peak', 'C', 0)
			i1, p1 = self.previous_optima ('peak', 'C', 1)
			if p0 is not None and p1 is not None:
				ptrend = 'rising' if p0 > p1
		i0, c0 = self.previous_optima ('cayon', 'C', 0)
		i1, c1 = self.previous_optima ('cayon', 'C', 0)
		i0, p0 = self.previous_optima ('peak', 'C', 0)
		i1, p1 = self.previous_optima ('peak', 'C', 0)

		if c1 is not None and c0 is not None:
			if c1 > c0:
		
		self.prediction ['trend'] = ptrend
		
		return ptrend

	def predict_profitable (self, data):
		# SD >= goal
		# Desired point:  canyon
		sd = ta.sSD (self.pdarchieve, 6, 'C', MA_Type.SMA)[self.archieve_len-1]
		
		#expected_goal_archieved =  sd > (self._goal * data['Last'])
		expected_goal_archieved  = True
		trend_
		bearish_signal  = ((self.predict('trend',data) == 'canyon') or (self.predict('trend',data) == 'rising' and self.pre_ptrend == 'falling')) and 
		if profitable:
			print ('Predict trend {t} - previous predicted trend {pt}'.format(t = self.predict('trend',data), pt = self.pre_ptrend))
			print ('SD {0:20}'.format(sd))
			print ('Price at goal = ' + str((1 + self._goal) * data['Last']))
			
		return profitable

	def predict_harvestable (self, data):
		# sell at goal
		# rising trending is finished
		trend_done = self.predict('trend',data) == 'peak' or self.predict('trend',data) == 'falling'
		return self.check_goal_achieved (data['Last']) and trend_done
