import environs
from pycoingecko import CoinGeckoAPI
from telebot import TeleBot

env = environs.Env()
env.read_env('.env')

BOT_TOKEN = env('BOT_TOKEN')

bot = TeleBot(token=BOT_TOKEN)
coin_client = CoinGeckoAPI()


#print(coin_client.get_price(ids='bitcoin', vs_currencies='usd')['bitcoin']['usd'])

@bot.message_handler(content_types=['text'])
def crypto_price_message_handler(message):
    crypto_id = (message.text).lower()
    crypto_idbig = crypto_id.upper()
    priceresponse = coin_client.get_price(ids=crypto_id, vs_currencies='usd', include_market_cap=True, include_24hr_vol=True, include_24hr_change=True)

    if priceresponse:
        price = priceresponse[crypto_id]['usd']
        marketcap = priceresponse[crypto_id]['usd_market_cap']
        volume = priceresponse[crypto_id]['usd_24h_vol']
        change = priceresponse[crypto_id]['usd_24h_change']

        bot.send_message(chat_id=message.chat.id, text=f"{crypto_idbig}\\USD = {price} | MarketCap = {marketcap} Volume = {volume} Change = {change}")
    else:
        bot.send_message(chat_id=message.chat.id, text=f"{crypto_idbig}\\USD was not found")


if __name__ == '__main__':
    bot.polling()
