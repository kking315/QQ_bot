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


def get_city_weather(selected_cities):
    # 获取选定城市的实时天气数据
    for city in selected_cities:
        live_data = fetch_weather_data(city['code'], 'base')
        if live_data and 'lives' in live_data:
            for live in live_data['lives']:
                date = live.get('reporttime', 'N/A')
                temperature = f"{live.get('temperature', 'N/A')}°C"
                humidity = f"{live.get('humidity', 'N/A')}%"
                winddirection = live.get('winddirection', 'N/A')
                windpower = live.get('windpower', 'N/A')
                weather = live.get('weather', 'N/A')
                all_live_data.append([city['name'], date, temperature, humidity, winddirection, windpower, weather])

    # 获取选定城市的预报天气数据
    for city in selected_cities:
        forecast_data = fetch_weather_data(city['code'], 'all')
        if forecast_data and 'forecasts' in forecast_data:
            for forecast in forecast_data['forecasts'][0]['casts']:
                date = forecast.get('date', 'N/A')
                high_temperature = f"{forecast.get('daytemp', 'N/A')}°C"
                low_temperature = f"{forecast.get('nighttemp', 'N/A')}°C"
                day_weather = forecast.get('dayweather', 'N/A')
                night_weather = forecast.get('nightweather', 'N/A')
                day_wind = forecast.get('daywind', 'N/A')
                night_wind = forecast.get('nightwind', 'N/A')
                all_forecast_data.append(
                    [city['name'], date, high_temperature, low_temperature, day_weather, night_weather, day_wind,
                     night_wind])


def format_weather_message(all_live_data, all_forecast_data):
    message = "**天气信息**\n\n"

    # 添加实时天气信息
    message += "## 实时天气\n"
    for live in all_live_data:
        message += f"**日期：{live[1]}**\n"
        message += f"城市: {live[0]}\n"
        message += f"温度: {live[2]}\n"
        message += f"湿度: {live[3]}\n"
        message += f"风向: {live[4]}\n"
        message += f"风力: {live[5]}\n"
        message += f"天气: {live[6]}\n\n"

    # 添加预报天气信息
    message += "## 预报天气\n"
    for forecast in all_forecast_data:
        message += f"**日期：{forecast[1]}**\n"
        message += f"城市: {forecast[0]}\n"
        message += f"最高温度: {forecast[2]}\n"
        message += f"最低温度: {forecast[3]}\n"
        message += f"白天天气: {forecast[4]}\n"
        message += f"夜间天气: {forecast[5]}\n"
        message += f"白天风向: {forecast[6]}\n"
        message += f"夜间风向: {forecast[7]}\n\n"

    return message


if __name__ == "__main__":
    # 用户可以选择要查询的城市
    selected_cities = [city for city in cities if input(f"是否查询 {city['name']} 的天气？ (y/n): ").lower() == 'y']

    if not selected_cities:
        print("没有选择任何城市。")
    else:
        get_city_weather(selected_cities)

        # 构建天气信息的消息
        message = format_weather_message(all_live_data, all_forecast_data)

        # 发送 POST 请求
        response = requests.post('http://localhost:3000/send_private_msg', json={
            'user_id': 895686378,
            'message': [
                {
                    'type': 'text',
                    'data': {
                        'text': message
                    }
                }
            ]
        })

        # 打印响应状态码和内容
        print(f"Status Code: {response.status_code}")
        print(f"Response Text: {response.text}")
