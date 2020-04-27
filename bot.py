import telebot
import requests
import json
import markdown

telebot.apihelper.proxy = {'https': 'socks5://geek:socks@t.geekclass.ru:7777'}
bot = telebot.TeleBot('1130697575:AAH9JvrBOy_wykEjf3l3v87xtqGXGAVO_SQ')


@bot.message_handler(commands=['start'])
def main_commands(message):
    bot.send_sticker(message.chat.id, "CAACAgIAAxkBAAJehF6nItN2v8Nd4nI1z1O5m_JdJPppAALYAQACVp29CpjUfylnzkA5GQQ")
    bot.send_message(message.chat.id, '*Welcome to the weather-bot. ' + '\n'
                                      'All you have to do is enter the name of the locality. ' + '\n'
                                      'The bot displays the weather in this place.*'.format(message.from_user, bot.get_me()), parse_mode='markdown')


@bot.message_handler(content_types=['text'])
def city(message):
    line = message.text.replace(' ', '')
    url = 'http://api.openweathermap.org/data/2.5/weather?q='+line+'&appid=a2dc81d271fabe25888d2ec5319edc31'
    response = requests.get(url)
    data = json.loads(response.text)

    if data["cod"] == 200:
        bot.send_message(message.chat.id, "Weather in *"+data["name"]+"* :\n"
                         "*Temperature*: "+str(round(data["main"]["temp"]-273)) + "°C\n"
                         "*Feels like*: "+str(round(data["main"]["feels_like"])-273) + "°C\n"
                         "*Wind:* " + str(data["wind"]["speed"]) + " m/sec" + "\n"
                         "*Pressure:* " + str(round(data["main"]["pressure"]*0.75)) + " mm of mercury\n"
                         "*Humidity:* " + str(round(data["main"]["humidity"])) + "%\n"
                         "*Description:* " + data["weather"][0]["description"] + "\n"
                         "*Clouds:* " + str(data["clouds"]["all"]) + "%".format(message.from_user, bot.get_me()), parse_mode='markdown')
    else:
        bot.send_message(message.chat.id, "*Check that the data you entered is correct.*"
                         .format(message.from_user, bot.get_me()), parse_mode='markdown')
        bot.send_sticker(message.chat.id,"CAACAgIAAxkBAAJejV6nVwsv_dzmBguPnjtf3nAmbupKAALjAQACVp29Cg-8gyoIanaVGQQ")


bot.polling()