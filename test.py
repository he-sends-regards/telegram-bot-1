import requests
from bs4 import BeautifulSoup

headers = {'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Safari/605.1.15'}
meteopost_data = 'https://meteopost.com/weather/kiev/'
meteopost_page = requests.get(meteopost_data, headers = headers)
meteopost_soup = BeautifulSoup(meteopost_page.content, 'html.parser')
meteopost_convert = meteopost_soup.findAll('span', {'class': 'dat'})
humidity_page = requests.get(meteopost_data, headers = headers)
humidity_value = meteopost_convert[3].text

if int(humidity_value[0:humidity_value.find('%')]) >= 30 and int(humidity_value[0:humidity_value.find('%')]) <= 60:
    print('Влажность в норме')
elif int(humidity_value[0:humidity_value.find('%')]) < 30:
    print('Влажность понижена')
elif int(humidity_value[0:humidity_value.find('%')]) > 60:
    print('Влажность повышена')
