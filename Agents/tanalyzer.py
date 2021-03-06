from . import misc_utils as misc

class TAnalyzer (misc.BPA):
	def __init__ (self, source, agents, params):
		misc.BPA.__init__ (self, source = source)
		self.seeker  = agents ['seeker']

		self.is_idle = True

		self.seeker.setParams (params)

	def setShoutFunc (self, func):
		misc.BPA.setShoutFunc (self, func)
		self.seeker.setShoutFunc (func)

	def CallBack (self, data):
		new_data = data.copy ()

		profitable = self.seek_oppoturnity (data)
		harvestable = self.check_harvestable (data)

		d0 = 'buy' if profitable else None
		d1 = 'sell' if harvestable else None
		new_data ['act'] = [[d0, d1]]
		new_data ['calculations'] = self.seeker.last_calculations_ans.copy ()
		self.BroadCast (new_data)

	def seek_oppoturnity (self, data):
		predict_profitable = self.seeker.predict ('profitable', data)
		return predict_profitable 

	def check_harvestable (self, data):
		predict_harvestable = self.seeker.predict ('harvestable', data)
		return predict_harvestable
