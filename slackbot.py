import datetime
import slack
import os
import yfinance as yf
from pathlib import Path
from dotenv import load_dotenv
from flask import Flask
from slackeventsapi import SlackEventAdapter

#tickers_list = ["VOO"]
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

#app = current running server
app = Flask(__name__)
slack_event_adapter = SlackEventAdapter(
    os.environ['SIGNING_SECRET'], '/slack/events', app)

client = slack.WebClient(os.environ['TOKEN'])

#if bot is sending message, dont respond. Only respond to users
BOT_ID = client.api_call("auth.test")['user_id']

def get_data(ticker):
    ticker_data = yf.Ticker(ticker)

    # ticker_info holds all the data from the company
    # holds in a dictionary.
    ticker_info = ticker_data.info
    comp_name = ticker_info['shortName'] #for apple, gets "Apple Inc."
    print(comp_name)

    # get stock values for current day
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

@slack_event_adapter.on('message')
def message(payload):  #when message is sent, take and handle payload
    event = payload.get('event', {})
    channel_id = event.get('channel')
    user_id = event.get('user')
    text = event.get('text')

    if BOT_ID != user_id:
        client.chat_postMessage(channel=channel_id, text=get_data(text))

if __name__ == '__main__':
    app.run(debug=True)


