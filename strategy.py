import misc_utils as misc
import trader_cfg as cfg
from time import time

class Strategy (misc.BPA):
	def __init__ (self, source, agents, params, risk_mgnt):
		misc.BPA.__init__ (self, source = source)
		self.seeker  = agents ['seeker']
		self.risky   = risk_mgnt
		
		self.is_idle = True

		self.feeling_lucky = params ['i_am_lucky'] # TODO: for fun

		self.seeker.setParams (params)
		self.risky.setParams  (params)

	def CallBack (self, data):
		new_data = data.copy ()
		turn = False
		
		if self.is_idle:
			predict, profitable = self.seek_oppoturnity (data)
			act = ['buy', data ['T']] if profitable else [None]
			new_data ['act']        = act
			new_data ['predict']    = predict
			turn = act [0] == 'buy'

		else:
			risk, goal_achieved, predict, harvestable = self.check_harvestable (data)
			if risk:
				print ('Risk {r}'.format(r=risk))
				act = ['sell'] if predict == 'falling' or predict == 'peak' else [None]
			else:
				act = ['sell'] if harvestable else [None]
			turn = act [0] == 'sell'
				
			new_data ['act'] = act
			new_data ['predict'] = predict 	 

		self.BroadCast (new_data)

		self.is_idle = not self.is_idle if turn else self.is_idle
				
	def seek_oppoturnity (self, data):
		predict_trend      = self.seeker.predict ('trend', data)
		predict_profitable = self.seeker.predict ('profitable', data)
		return (predict_trend, predict_profitable) 

	def check_harvestable (self, data):
		risk                = self.risky.check_risk (data['Last'])
		predict_trend       = self.seeker.predict ('trend', data)
		predict_harvestable = self.seeker.predict ('harvestable', data)
		goal_achieved       = self.seeker.predict ('hitgoal', data)
		return (risk, goal_achieved, predict_trend, predict_harvestable)
