from telegram.ext import (Updater, CommandHandler, CallbackQueryHandler, Filters, BaseFilter)
from telegram.error import (TelegramError, Unauthorized, BadRequest, TimedOut, ChatMigrated, NetworkError)
from telegram import (InlineKeyboardButton, InlineKeyboardMarkup)
import logging

from time import (localtime, strftime)
from datetime import datetime

from threading import Thread, Event
from queue import Queue

import acts_config as cfg

answerQueue = Queue (maxsize = 1)

class UBot:
	act_name    = ""
	act_chat_id = ""
	act_bot     = None

	updater     = None 
	dispatcher  = None
	
	workable = False

	def error_cb (self, bot, update, error):
		try:
			raise error
		except Unauthorized:
			print ("Unauthorized") 
		except BadRequest:
			print ("Malformed requests")
		except TimedOut:
			print ("Slow connection")
		except NetworkError:
			print ("Network error")
		except ChatMigrate as e:
			print ("Chat ID of group has changed") 
		except TelegramError:
			print ("Internal Telegram error")

	def is_allowed (bot, update):
		if update.message.chat_id != self.act_chat_id:
			bot.send_message (update.message.chat_id, text = "I don't know you. You're harrasing.")
			return False
		else:
			return True

	def respond (self, texts, **kwargs):
		"""
		In case of Markdown or HTML, the split feature would cause error due to no matching parentheses.
		So that feature is abandoned if Markdown or HTML exists
		"""
		if type(texts) is list:
			for idx, text in enumerate(texts):
					self.act_bot.send_message (self.act_chat_id, text = text, **kwargs)
		else:
			self.act_bot.send_message (self.act_chat_id, text = texts, **kwargs)

	def initialize (self, bot, update):
		#self.act_chat_id = update.message.chat_id
		self.act_bot     = bot
		self.greeting ()
		self.workable = True
		#print (self.act_chat_id)
		#print (update.message.chat_id)
	
	def greeting (self):
		h = datetime.now().time().hour
		if h >= 5 and h <= 12:
			greeting = "Good morning."
		elif h > 12 and h <= 17:
			greeting = "Good afternoon."
		elif h > 17 and h <= 21:
			greeting = "Good evening."
		else:
			greeting = "Greetings night owl."
	
		self.respond (greeting + " " + "My name is " + self.act_name)

	def live (self):
		self.updater.start_polling()
		
	def stop (self):
		self.updater.stop ()
		self.respond ("I'm offline right now. Good bye.")

	def add_handler (self, hndl):
		self.dispatcher.add_handler (hndl)

	def remove_handler (self, hndl):
		self.dispatcher.remove_handler (hndl)

	def __init__ (self, name = "ACTS"):
		self.act_name = name 
		self.updater    = Updater(token=cfg.config['Telegram']['token'], request_kwargs={'proxy_url': cfg.config['Telegram']['proxy_url']})
		self.act_chat_id    = int(cfg.config['Telegram']['chat_id'])
		self.dispatcher = self.updater.dispatcher

		self.dispatcher.add_error_handler (self.error_cb)
		logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
		
tbot = UBot ()

def start (bot, update):
	tbot.initialize (bot, update)
	
def notify (text):
	tbot.respond (text)
	
def ask_confirm (question_text):
	buttons = [[InlineKeyboardButton ("Yes", callback_data = 'yes'), InlineKeyboardButton ("No", callback_data = 'no')]]
	buttonsMarkup = InlineKeyboardMarkup  (buttons)
	tbot.respond (question_text, reply_markup = buttonsMarkup)
	
def answer (bAns):
	print (bAns)
	answerQueue.put (bAns, block = True)
	
def query_func (bot, update):
	query = update.callback_query
	if query.data == 'yes':
		answer (True)
	else:
		answer (False)
	bot.edit_message_text (text = 'You answered {ans}'.format (ans = query.data), chat_id = query.message.chat_id, message_id = query.message.message_id)
	return
	
def stop_bot ():
	tbot.stop ()
	
class FilterMe (BaseFilter):
	def filter (self, message):
		if message.chat_id != tbot.act_chat_id:
			return False
		else:
			return True
	
filterme = FilterMe ()

cmd_start_hndl = CommandHandler ('start', start, filters = filterme)
qry_yesno_hndl = CallbackQueryHandler (query_func)
tbot.add_handler (cmd_start_hndl)
tbot.add_handler (qry_yesno_hndl)