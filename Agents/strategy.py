from . import misc_utils as misc

class Strategy (misc.BPA):
	def __init__ (self, source, agents, params, risk_mgnt):
		misc.BPA.__init__ (self, source = source)
		self.seeker  = agents ['seeker']
		self.risky   = risk_mgnt
		
		self.is_idle = True

		self.seeker.setParams (params)
		self.risky.setParams  (params)

	def setShoutFunc (self, func):
		misc.BPA.setShoutFunc (self, func)
		self.seeker.setShoutFunc (func)
		self.risky.setShoutFunc (func)

	def performed_well (self, data):
		self.is_idle = not self.is_idle if data == True else self.is_idle

	def CallBack (self, data):
		new_data = data.copy ()
		turn = False
		act = [None]
		predict = 'rising'

		if self.is_idle:
			predict, profitable = self.seek_oppoturnity (data)
			act = ['buy', data ['T']] if profitable else [None]

		else:
			risk, goal_achieved, predict, harvestable = self.check_harvestable (data)
			if risk:
				#self.shout ('Risk {r}'.format(r=risk))
				act = ['sell', data ['T']]# if predict == 'falling' or predict == 'peak' else [None]
			else:
				act = ['sell', data ['T']] if harvestable else [None]

		new_data ['act'] = act
		new_data ['predict'] = predict 	 
		new_data ['calculations'] = self.seeker.last_calculations_ans.copy ()
		self.BroadCast (new_data)


	def seek_oppoturnity (self, data):
		predict_trend      = self.seeker.predict ('trend', data)
		predict_profitable = self.seeker.predict ('profitable', data)
		return predict_trend, predict_profitable 

	def check_harvestable (self, data):
		risk                = self.risky.check_risk (data['Last'])
		predict_trend       = self.seeker.predict ('trend', data)
		predict_harvestable = self.seeker.predict ('harvestable', data)
		goal_achieved       = self.seeker.predict ('hitgoal', data)
		return risk, goal_achieved, predict_trend, predict_harvestable
