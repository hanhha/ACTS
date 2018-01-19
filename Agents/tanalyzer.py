from . import misc_utils as misc

class TAnalyzer (misc.BPA):
	def __init__ (self, source, agents, params, risk_mgnt):
		misc.BPA.__init__ (self, source = source)
		self.seeker  = agents ['seeker']
		
		self.is_idle = True

		self.seeker.setParams (params)

	def setShoutFunc (self, func):
		misc.BPA.setShoutFunc (self, func)
		self.seeker.setShoutFunc (func)

	def CallBack (self, data):
		new_data = data.copy ()
		predict = 'rising'
		
		predict_for_buy, profitable = self.seek_oppoturnity (data)
		goal_achieved, predict_for_sell, harvestable = self.check_harvestable (data)
				
		#TDOD: hha
		new_data ['act'] = act
		new_data ['predict'] = predict 	 
		self.BroadCast (new_data)

	def seek_oppoturnity (self, data):
		predict_trend      = self.seeker.predict ('trend', data)
		predict_profitable = self.seeker.predict ('profitable', data)
		return (predict_trend, predict_profitable) 

	def check_harvestable (self, data):
		predict_trend       = self.seeker.predict ('trend', data)
		predict_harvestable = self.seeker.predict ('harvestable', data)
		goal_achieved       = self.seeker.predict ('hitgoal', data)
		return (goal_achieved, predict_trend, predict_harvestable)
