import yfinance as yf
import datetime

#yf documentation
# https://pypi.org/project/yahoo-finance/

#tickers identify company
tickers = ["AAPL", "MSFT", "AMZN", "INTC", "VOO"]


def getData(ticker):
    tickerdata = yf.Ticker(ticker)
    #tickerinfo holds all the data from the company
    #holds in a dictionary.
    tickerinfo = tickerdata.info
    compName = tickerinfo['shortName'] #for apple, gets "Apple Inc."
    print(compName)

    #get stock values for current day
    todaysDate = datetime.datetime.today().isoformat()
    print('Today = ' + todaysDate)


    #get stock values for current certain time frame (this is month of oct)
    #outputs first 10 characters from todays date
    stockData = tickerdata.history(period='1d', start='2020-10-01', end=todaysDate[:10])


    #get most current stock price from closing cost, get the last one from stockData
    mostCurrentPrice = stockData['Close'].iloc[-1]

    #get last stock value to calculate change in value
    priceLast = stockData['Close'].iloc[-2]
    priceChange = priceLast - mostCurrentPrice

    #output data (currentPrice is float value, cast to string)
    print(compName + ' Last stock value = $' + str(mostCurrentPrice))
    print('Change in stock value = ' + str(priceChange))

#Run through tickers and output data
for ticker in tickers:
    getData(ticker)
    print('') #newline