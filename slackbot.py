# Run pip install slack_sdk to get this imported properly
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import yfinance as yf
import datetime

tickers_list = ["VOO"]


def get_data(ticker):
    ticker_data = yf.Ticker(ticker)

    # ticker_info holds all the data from the company
    # holds in a dictionary.
    ticker_info = ticker_data.info
    comp_name = ticker_info['shortName'] #for apple, gets "Apple Inc."
    print(comp_name)

    # get stock values for cuarrent day
    todays_date = datetime.datetime.today().isoformat()
    print('Today = ' + todays_date)

    # get stock values for current certain time frame (this is month of oct)
    # outputs first 10 characters from todays date
    stock_data = ticker_data.history(period='1d', start='2020-10-01', end=todays_date[:10])

    # get most current stock price from closing cost, get the last one from stockData
    most_current_price = stock_data['Close'].iloc[-1]

    # get last stock value to calculate change in value
    price_last = stock_data['Close'].iloc[-2]
    price_change = price_last - most_current_price

    # output data (currentPrice is float value, cast to string)
    print(comp_name + ' Last stock value = $' + str(most_current_price))
    print('Change in stock value = ' + str(price_change))

    return f"Name: {comp_name} \n Date: {todays_date} \n Current Price: {most_current_price} \n Price Change: {price_change} "


def send_message(msg):
    client = WebClient(token="xoxb-1483296803783-1504244788788-9erhtYRMdrVuB8a9hIluQpO0")

    try:
        response = client.chat_postMessage(channel='#general', text=msg)
    except SlackApiError as e:
        print(f"Got an error: {e.response['error']}")


if __name__ == '__main__':
    # Run through tickers and output data
    for ticker in tickers_list:
        send_message(get_data(ticker))
