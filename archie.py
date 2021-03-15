import discord
import requests
from configparser import ConfigParser
from datetime import datetime
from discord.ext import tasks

config = ConfigParser()
config.read('config.ini')
DISCORD_TOKEN = config['tokens']['discord']
Y_FINANCE_API = 'https://query2.finance.yahoo.com/v7/finance/options/'
client = discord.Client()


@client.event
async def on_message(message):
    if message.author != client.user:
        msg = message.content.split()
        try:
            if msg[0] == "!price":
                await message.channel.send(get_prices(msg[1:]))

            elif msg[0] == "!quote":
                await message.channel.send(get_quote(msg[1]))

            elif msg[0] == "!call":
                call_list = get_call(msg[1])
                for call in call_list:
                    await message.channel.send(call)

            elif msg[0] == "!put":
                put_list = get_put(msg[1])
                for put in put_list:
                    await message.channel.send(put)

        except IndexError:
            await message.channel.send("Please enter a valid ticker")


def get_prices(tickers):
    prices = list()
    seen = set()
    for ticker in tickers:
        if ticker not in seen:
            req = requests.get(Y_FINANCE_API + ticker)
            if req.status_code == 200:
                quote = req.json()['optionChain']['result'][0]['quote']
                prices.append("{}: {}".format(ticker.upper(), quote['regularMarketPrice']))
    return ", ".join(prices)


def get_quote(ticker):
    req = requests.get(Y_FINANCE_API + ticker)
    if req.status_code == 200:
        quote = req.json()['optionChain']['result'][0]['quote']
        return "\n".join(["{}: {}".format(key, value) for key, value in quote.items()])


def get_call(ticker):
    call_list = list()
    req = requests.get(Y_FINANCE_API + ticker)
    if req.status_code == 200:
        calls = req.json()['optionChain']['result'][0]['options'][0]['calls']
        for call in calls:
            call_info = list()
            for key, value in call.items():
                if key in ('expiration', 'lastTradeDate'):
                    value = datetime.fromtimestamp(value).strftime("%m/%d/%Y")
                call_info.append("{}: {}".format(key, value))
            call_list.append("\n".join(call_info))
    return call_list


def get_put(ticker):
    put_list = list()
    req = requests.get(Y_FINANCE_API + ticker)
    if req.status_code == 200:
        puts = req.json()['optionChain']['result'][0]['options'][0]['puts']
        for put in puts:
            put_info = list()
            for key, value in put.items():
                if key in ('expiration', 'lastTradeDate'):
                    value = datetime.fromtimestamp(value).strftime("%m/%d/%Y")
                put_info.append("{}: {}".format(key, value))
            put_list.append("\n".join(put_info))
    return put_list

client.run(DISCORD_TOKEN)