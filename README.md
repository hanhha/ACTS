# Auto crypto coin trading system #

This can help to trade crypto coin on exchange (currently support Bittrex only) basing on user customized strategy. It supports trial mode in that the trading decision will be simulated with real market data.

## Usage guide ##

### Install ###
- Download or clone the repository and run directly inside.

### Usage guide ###
- Create seeker_custom.py file and extend the BaseSeeker class using below template:
~~~
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
- Modify trader_cfg.py to specify your desired parameters as guided inside.

### Requirements ###
- Python 3+.
- My [Bittrex API Python wrapper](https://github.com/hanhha/bittrex).
- You may want to use TA-Lib for technical analysis. I suggest [this wrapper](https://mrjbq7.github.io/ta-lib/).
