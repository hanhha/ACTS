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

		new_data ['profitable'] = profitable
		new_data ['harvestable'] = harvestable
		self.BroadCast (new_data)

	def seek_oppoturnity (self, data):
		predict_profitable = self.seeker.predict ('profitable', data)
		return predict_profitable 

	def check_harvestable (self, data):
		predict_harvestable = self.seeker.predict ('harvestable', data)
		return predict_harvestable
