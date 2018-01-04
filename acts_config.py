import configparser as CfgPsr

config = CfgPsr.ConfigParser ()
config.read ('acts_config.ini')

telegram_en = True if 'Telegram' in config.keys() else False
