import configparser as CfgPsr
import os

config = None

if os.path.isfile ('acts_config.ini'):
	config = CfgPsr.ConfigParser ()
	config.read ('acts_config.ini')
else:
	print ("It seems that this is your first time :)")
	print ("Welcome. Currently I'm able to trade on Bittrex exchange only.")
	print ("I need Bittrex's API key and secret with appropriate permission. Please give me those info.")
	api_key    = input ('Please input your API Key of your Bittrex representative: ')
	api_secret = input ('Please input your API Secret of your Bittrex representative: ')
	print ("Creating your config file, please wait ...")
	ok = False
	try:
		with open ("acts_config.ini", "w+") as cf:
			cf.write ('[Bittrex]\n')
			cf.write ('API_KEY = ' + api_key + '\n')
			cf.write ('API_SECRET = ' + api_secret + '\n')
		ok = True
	except IOError:
		print ("Can not save config file.")
	if not ok:
		print ("No config file saved. I can not help to trade, but still be able to query public info.")
		config = {'Bittrex':{'API_KEY':'nokey','API_SECRET':'nosecret'}}
	else:
		print ("Thanks. Hope we will work together well.")
		config = CfgPsr.ConfigParser ()
		config.read ('acts_config.ini')

telegram_en = True if 'Telegram' in config.keys() else False
