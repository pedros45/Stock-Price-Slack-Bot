# Run pip install slack_sdk to get this imported properly
import datetime
import slack
import os
import yfinance as yf
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from pathlib import Path
from dotenv import load_dotenv
from flask import Flask
from slackeventsapi import SlackEventAdapter

#install ngrok to run bot from local server on pc
#takes public IP address/domain and routes it to our local server
#https://ngrok.com/download
#This will allow us to a server on our local computer
#Takes public IP address/domain and routes that to our local server
#

#install micro web service "flask"
#pip install flask
#pip install slackeventsapi

#Run engrok, enter command: ngrok http 127.0.0.1:5000
#Check forwarding line, mine says:
#http://43d1cd57d0ae.ngrok.io -> http://localhost:5000
#Takes public IP address, and points to our local host web server address
#Keep running during development

#Enable events on slack api app
#Request URL:  when an event occurs,
#the slack API is going to send a post request to our web server.
#From here we can get the request and handle it accordingly.
#Take URL from ngrok and past it into REQUEST URL, append /slack/events
#Mine looks like:  http://43d1cd57d0ae.ngrok.io/slack/events
#Python code and ngrok should be running this time for slack API to verify url
#Slack API website, Subscribe to bot events -> Add Bot User Event ->
#enter: message.channels
#when someone sends a message, sends to our URL where we can handle event
#save changes.


tickers_list = ["VOO"]
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

#app = current running server
app = Flask(__name__)
slack_event_adapter = SlackEventAdapter(
    os.environ['SIGNING_SECRET'], '/slack/events', app)


client = slack.WebClient(os.environ['TOKEN'])
client.chat_postMessage(channel='#test', text="TestingBot")

if __name__ == '__main__':
    #if file ran directly, run web server on default port 5000
    app.run(debug=True)
    # Run through tickers and output data
    #for ticker in tickers_list:
        #send_message(get_data(ticker))


# def get_data(ticker):
#     ticker_data = yf.Ticker(ticker)
#
#     # ticker_info holds all the data from the company
#     # holds in a dictionary.
#     ticker_info = ticker_data.info
#     comp_name = ticker_info['shortName'] #for apple, gets "Apple Inc."
#     print(comp_name)
#
#     # get stock values for current day
#     todays_date = datetime.datetime.today().isoformat()
#     print('Today = ' + todays_date)
#
#     # get stock values for current certain time frame (this is month of oct)
#     # outputs first 10 characters from todays date
#     stock_data = ticker_data.history(period='1d', start='2020-10-01', end=todays_date[:10])
#
#     # get most current stock price from closing cost, get the last one from stockData
#     most_current_price = stock_data['Close'].iloc[-1]
#
#     # get last stock value to calculate change in value
#     price_last = stock_data['Close'].iloc[-2]
#     price_change = price_last - most_current_price
#
#     # output data (currentPrice is float value, cast to string)
#     print(comp_name + ' Last stock value = $' + str(most_current_price))
#     print('Change in stock value = ' + str(price_change))
#
#     return f"Name: {comp_name} \n Date: {todays_date} \n Current Price: {most_current_price} \n Price Change: {price_change} "
#
#
# def send_message(msg):
#     client = slack.WebClient(os.environ['TOKEN'])
#     BOT_ID = client.api_call("auth.text")["user_id"]    #returns ID of bot
#
#
#     @slack_event_adapter.on('message')
#     def message(payload):  #when message is sent, take and handle payload
#         event = payload.get('event', {})
#         channel_id = event.get('channel')
#         user_id = event.get('user')
#         text = event.get('text')
#
#         #determine if message being read is from user or from the bot
#         if BOT_ID != user_id:
#             client.chat_postMessage(channel=channel_id, text=text)
#
#     try:
#         response = client.chat_postMessage(channel='#test', text="TestingBot")
#     except SlackApiError as e:
#         print(f"Got an error: {e.response['error']}")
#
#
# if __name__ == '__main__':
#     #if file ran directly, run web server on default port 5000
#     app.run(debug=True)
#     # Run through tickers and output data
#     #for ticker in tickers_list:
#         #send_message(get_data(ticker))


