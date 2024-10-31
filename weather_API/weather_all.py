import requests
from tabulate import tabulate

# 高德地图API URL
url = 'https://restapi.amap.com/v3/weather/weatherInfo'

# 请求参数模板
params_template = {
    'key': '******',  # 提供的高德地图API密钥
    'output': 'JSON'  # 返回格式为JSON
}

# 城市列表及其编码
cities = [
    {'name': '武汉市', 'code': '420100'},
    {'name': '长沙市', 'code': '430100'}
]

# 存储所有城市的天气数据
all_live_data = []
all_forecast_data = []


def fetch_weather_data(city_code, extensions):
    params = params_template.copy()
    params['city'] = city_code
    params['extensions'] = extensions

    response = requests.get(url, params=params)

    if response.status_code == 200:
        weather_data = response.json()

        if weather_data.get('status') == '1':
            return weather_data
        else:
            print(f"{city_code} API请求失败: {weather_data.get('info', '未知错误')}")
    else:
        print(f"{city_code} HTTP请求失败，状态码: {response.status_code}")

    return None


# 获取所有城市的实时天气数据
for city in cities:
    live_data = fetch_weather_data(city['code'], 'base')
    if live_data and 'lives' in live_data:
        for live in live_data['lives']:
            date = live.get('reporttime', 'N/A')
            temperature = live.get('temperature', 'N/A')
            humidity = live.get('humidity', 'N/A')
            winddirection = live.get('winddirection', 'N/A')
            windpower = live.get('windpower', 'N/A')
            weather = live.get('weather', 'N/A')
            all_live_data.append([city['name'], date, temperature, humidity, winddirection, windpower, weather])

# 获取所有城市的预报天气数据
for city in cities:
    forecast_data = fetch_weather_data(city['code'], 'all')
    if forecast_data and 'forecasts' in forecast_data:
        for forecast in forecast_data['forecasts'][0]['casts']:
            date = forecast.get('date', 'N/A')
            high_temperature = forecast.get('daytemp', 'N/A')
            low_temperature = forecast.get('nighttemp', 'N/A')
            day_weather = forecast.get('dayweather', 'N/A')
            night_weather = forecast.get('nightweather', 'N/A')
            day_wind = forecast.get('daywind', 'N/A')
            night_wind = forecast.get('nightwind', 'N/A')
            all_forecast_data.append(
                [city['name'], date, high_temperature, low_temperature, day_weather, night_weather, day_wind,
                 night_wind])

# 打印实时天气数据表
if all_live_data:
    print("\n实时天气数据:")
    print(tabulate(all_live_data, headers=['城市', '日期', '温度', '湿度', '风向', '风力', '天气'], tablefmt='pretty'))

# 打印预报天气数据表
if all_forecast_data:
    print("\n预报天气数据:")
    print(tabulate(all_forecast_data,
                   headers=['城市', '日期', '最高温', '最低温', '白天天气', '夜间天气', '白天风向', '夜间风向'],
                   tablefmt='pretty'))
