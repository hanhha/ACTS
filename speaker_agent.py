#!/usr/bin/env python3

from telegram.ext import (Updater, CommandHandler, CallbackQueryHandler)
from telegram.error import (TelegramError, Unauthorized, BadRequest, TimedOut, ChatMigrated, NetworkError)

import acts_bot as chatbot

import acts_config as cfg

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
				chatbot.notify (info_str)
			else:
				if type(info) is tuple:
					if info[0] is True:
						chatbot.notify (str (info[1][params[0]]))
					else:
						chatbot.notify (info[1])
				else:
					if info is True:
						chatbot.notify (str(param[0]))
			inpQ.task_done ()

def cfrm (inpQ, outQ, params, Stop):
	question = params [0]
	
	while not Stop.is_set ():
		if not inpQ.empty():
			tmp = inpQ.get (block = False)
			chatbot.ask_confirm (question)
			ans = chatbot.answerQueue.get (block = True)
			print ('User answered: {ans}'.format(ans=ans))
			if ans is True:
				for q in outQ:
					q.put (True, block = True)
			inpQ.task_done ()
			
def stop ():
	chatbot.tbot.stop ()
	
def workable ():
	return chatbot.tbot.workable
	
chatbot.tbot.live ()