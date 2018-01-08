#!/usr/bin/env python3

import acts_config as cfg

if cfg.telegram_en:
	import acts_bot as chatbot
	
def call_notify (text):
	if cfg.telegram_en:
		chatbot.notify (text)
	else:
		print (text)

def call_ask_confirm (text):
	if cfg.telegram_en:
		chatbot.ask_confirm (text)
		return chatbot.answerQueue.get (block = True)
	else:
		return True if raw_input (text) == 'yes' else False
		
def notf (inpQ, outQ, params, Stop):
	if params[0] == 'rem':
		fix_str = True
		info_str = params[1]
	else:
		fix_str = False

	while not Stop.is_set ():
		if not inpQ.empty():
			info = inpQ.get (block = False)
			if fix_str:
				call_notify (info_str)
			else:
				if type(info) is tuple:
					if info[0] is True:
						call_notify (str (info[1][params[0]]))
					else:
						call_notify (info[1])
				else:
					if info is True:
						call_notify (str(param[0]))
			inpQ.task_done ()

def cfrm (inpQ, outQ, params, Stop):
	question = params [0]
	
	while not Stop.is_set ():
		if not inpQ.empty():
			tmp = inpQ.get (block = False)
			ans = call_ask_confirm (question)
			#print ('User answered: {ans}'.format(ans=ans))
			if ans is True:
				for q in outQ:
					q.put (True, block = True)
			inpQ.task_done ()
			
def stop ():
	if cfg.telegram_en:
		chatbot.tbot.stop ()
	
def workable ():
	return chatbot.tbot.workable if cfg.telegram_en else True
	
if cfg.telegram_en:
	chatbot.tbot.live ()