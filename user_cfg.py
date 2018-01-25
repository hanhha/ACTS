from localconfig import LocalConfig 
import os

config = None
gain_loss_rules   = dict ()
market_attributes = dict ()
monitor_conf      = dict ()
debug_cfg         = dict ()

if os.path.isfile ('user_config.ini'):
	config = LocalConfig ('user_config.ini')

	gain_loss_rules   = dict(list(config.gain_loss_rules))
	market_attributes = dict(list(config.market_attributes))
	monitor_conf      = dict(list(config.monitor_conf))
	debug_cfg         = dict(list(config.debug_cfg))

else:
	print ("There is no user config file.")
	print ("I will create an empty config file for you then exit.")

	ok = False
	try:
		with open ("user_config.ini", "w+") as cf:
			cf.write ('[gain_loss_rules]\n')
			cf.write ('goal       = \n')
			cf.write ('loss       = \n')
			cf.write ('buy        = \n')
			cf.write ('sell       = \n')
			cf.write ('price      = \n')
			cf.write ('i_am_lucky = \n')
			cf.write ('\n')

			cf.write ('[monitor_conf]\n')
			cf.write ('interval   = \n')
			cf.write ('market     = \n')
			cf.write ('\n')

			cf.write ('[market_attributes]\n')
			cf.write ('fee        = \n')
			cf.write ('\n')

			cf.write ('[debug_cfg]\n')
			cf.write ('trial           = yes\n')
			cf.write ('simulation      = yes\n')
			cf.write ('initial_capital = 100\n')
		ok = True
	except IOError:
		print ("Can not save config file.")
	
	if not ok:
		print ("No config file saved. Please check and start again.")

	else:
		print ("An empty user config file has been created: user_config.ini.")
		print ("Please fulfill empty config file and start again.")

	exit (1)

