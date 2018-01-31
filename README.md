# Auto crypto coin trading system #

This can help to trade crypto coin on exchange (currently support Bittrex only) basing on user customized strategy. It supports trial mode in that the trading decision will be simulated with real market data.

## Usage guide ##

### Install ###
- Download or clone the repository and run directly inside.

### Usage ###
- Create seeker_custom.py file and extend the BaseSeeker class using below template:
~~~python
from Agents.seeker import BaseSeeker
class Seeker(BaseSeeker):
	#data is a dict that represent latest candle stick, current bid, ask and last price
	#{'C': close price, 'O': open price, 'H': highest price, 'L': lowest price', 'V': volume', 'BV': base volume', 'Bid': bid, 'Ask': ask, 'Last': last price}
	#history data is stored in self.archive (list type) and self.pdarchieve (pandas DataFrame type)
	
	def predict_profitable (self, data):
		<your code to return True if this is bullish signal>
		
	def predict_harvestable (self, data):
		<your code to return True if this is bearish signal>
		
	def predict_trend (self, data):
		<your code to return the prediction of trend which is among of ['peak', 'canyon', 'risng', 'falling', 'stable']>
~~~
- Run:
~~~
trader.py -h
~~~
For the first time, it would create 2 config files. You would then need to modify those files to match your desires.

+ user_config.ini : your desired market, goal, lost threshold, interval, exchange fee and some debug/simulation configuration.
+ acts_config.ini : API key and secret key for exchange, Bokeh configuration (in case that you want to show charts)

### Requirements ###
- Python 3.6+ (mandatory to show UI correctly)
- My [Bittrex API Python wrapper](https://github.com/hanhha/bittrex).
- My [Curses UI generator](https://github.com/hanhha/console_ui)
- You may want to use TA-Lib for technical analysis. I suggest [this wrapper](https://mrjbq7.github.io/ta-lib/).
- Bokeh to show the charts.
