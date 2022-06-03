import requests
import json
import time

apikey = "0276eeb82a71d9b7c07ce64e78fc7a3a"

city_list = ["Seoul"]

api = "https://api.openweathermap.org/data/2.5/weather?q={city}&APPID={key}"

k2C = lambda k: k - 273.15

for name in city_list:
	url = api.format(city = name, key = apikey)
	res = requests.get(url)
	data = json.loads(res.text)
	print("일몰시간 = ", data["sys"]["sunset"])
	print("현재시간 =", time.time())
