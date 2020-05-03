import random
import pyowm
import telebot
import datetime
import time
import requests
from bs4 import BeautifulSoup

owm = pyowm.OWM('6d00d1d4e704068d70191bad2673e0cc', language='ru')
bot = telebot.TeleBot('1042683676:AAFEXKnt_5F9iw1HOKuzlU7geZTVahGIodM')

#===================
# Weather showing ==
#===================
@bot.message_handler(commands=['weather_now'])
def send_weather(message):
    observation = owm.weather_at_place('Kyiv')
    forecast = owm.three_hours_forecast('Kyiv')
    w = observation.get_weather()
    temp = round(w.get_temperature('celsius')["temp"])
    now = datetime.datetime.now()
    answer = 'Сегодня: ' + str(now.strftime("%d.%m.%Y")) + ', время: ' + str(now.strftime('%H:%M')) + '\n' + "В Киеве сейчас " + w.get_detailed_status() + ", " + str(temp) + "°"
    bot.send_message(message.chat.id, answer)

#=========================================================
# Shows air pollution level, air pressure, and humidity ==
#=========================================================
@bot.message_handler(commands=['check_air'])
def check_air(message):
    headers = {'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Safari/605.1.15'}

    # POLLUTION
    iqAir_data = 'https://www.iqair.com/ukraine/kyiv'
    # Requests ReadTimeOut exception catching
    try:
        iqAir_page = requests.get(iqAir_data, headers = headers)
    except requests.exceptions.Timeout:
        iqAir_page = requests.get(iqAir_data, headers = headers)

    iqAir_soup = BeautifulSoup(iqAir_page.content, 'html.parser')
    iqAir_convert = iqAir_soup.findAll('span', {'class': 'aqi'})
    pollution_value = iqAir_convert[1].text
    bot.send_message(message.chat.id, 'Состояние воздуха в Киеве: ' + pollution_value + ', при норме в 50 единиц')

    analysis = ''
    if int(pollution_value) < 50:
        analysis = 'Уровень загрязнения - зелёный'
    elif int(pollution_value) > 50 and int(pollution_value) < 100:
        analysis = 'Уровень загрязнения - жёлтый'
    elif int(pollution_value) >= 100 and int(pollution_value) < 150:
        analysis = 'Уровень загрязнения - Оранжевый'
    elif int(pollution_value) >= 150 and int(pollution_value) < 250:
        analysis = 'Уровень загрязнения - Красный'
    else:
        analysis = 'Уровень загрязнения - экстримально высокий, будьте осторожны'
    bot.send_message(message.chat.id, analysis)
    
    # PRESSURE
    meteopost_data = 'https://meteopost.com/weather/kiev/'
    # Requests ReadTimeOut exception catching
    try:
        meteopost_page = requests.get(meteopost_data, headers = headers)
    except requests.exceptions.Timeout:
        meteopost_page = requests.get(meteopost_data, headers = headers)
    meteopost_soup = BeautifulSoup(meteopost_page.content, 'html.parser')
    meteopost_convert = meteopost_soup.findAll('span', {'class': 'dat'})

    
    pressure_full_value = meteopost_convert[5].text
    bot.send_message(message.chat.id, 'Давление воздуха: ' + pressure_full_value)

    NORMAL_PRESSURE = 746
    pressure_value = int(pressure_full_value[0:3])

    if (pressure_value == NORMAL_PRESSURE) or (NORMAL_PRESSURE - pressure_value > 0 and NORMAL_PRESSURE - pressure_value <= 20) or (NORMAL_PRESSURE - pressure_value < 0 and NORMAL_PRESSURE - pressure_value >= -20):
        bot.send_message(message.chat.id, 'Давление в норме')
    elif NORMAL_PRESSURE - pressure_value > 20:
        bot.send_message(message.chat.id, 'Давление пониженное')
    elif NORMAL_PRESSURE - pressure_value < -20:
        bot.send_message(message.chat.id, 'Давление повышенное')

    humidity_full_value = meteopost_convert[3].text
    bot.send_message(message.chat.id, 'Влажность воздуха: ' + humidity_full_value)

    humidity_value = int(humidity_full_value[0:humidity_full_value.find('%')])

    if humidity_value >= 30 and humidity_value <= 60:
        bot.send_message(message.chat.id, 'Влажность в норме')
    elif humidity_value < 30:
        bot.send_message(message.chat.id, 'Влажность понижена')
    elif humidity_value > 60:
        bot.send_message(message.chat.id, 'Влажность повышена')

    time.sleep(3600)
    check_air(message)


@bot.message_handler(commands=['finish_him'])
def finish_him(message):
    for i in range(100):
        bot.send_message(message.chat.id, '@doshik_ddt')
bot.polling(none_stop = True)