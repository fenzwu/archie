import discord
from configparser import ConfigParser
from iexfinance.stocks import Stock

config = ConfigParser()
config.read('config.ini')
DISCORD_TOKEN = config['tokens']['discord']
IEX_TOKEN = config['tokens']['iex']

client = discord.Client()


@client.event
async def on_message(message):
    if message.author != client.user:

        msg = message.content.split()

        if msg[0] == "$quote":
            await message.channel.send(get_quotes(msg[1:]))


def get_quotes(tickers):
    quotes = list()
    seen = set()
    for ticker in tickers:
        try:
            if ticker not in seen:
                stock = Stock(ticker, output_format='json', token=IEX_TOKEN)
                quotes.append("{}: {}".format(
                    ticker.upper(), stock.get_quote()['iexRealtimePrice']))
                seen.add(ticker)
        except:
            pass

    if quotes:
        return ", ".join(quotes)
    else:
        return "Please enter a valid ticker!"


client.run(DISCORD_TOKEN)
