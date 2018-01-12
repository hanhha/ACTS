#!/usr/bin/env python3

from talib import MA_Type
from Agents import ta
from Agents import misc_utils as misc
import pandas as pd
from talib import abstract
from Agents.seeker import BaseSeeker

class Seeker (BaseSeeker):
	def __init__ (self, source, params):
		BaseSeeker.__init__ (self, source, params)
		
	def predict_trend (self, data):
		#TODO: override this method
		return BaseSeeker.predict_trend (self, data)

	def predict_profitable (self, data):
		#TODO: override this method
		return BaseSeeker.predict_profitable (self, data)

	def predict_harvestable (self, data):
		#TODO: override this method
		return BaseSeeker.predict_harvestable (self, data)