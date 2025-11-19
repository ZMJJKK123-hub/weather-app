import requests
from config.settings import API_KEY, BASE_URL


def get_weather_data(city_name):
    """获取城市天气数据"""
    params = {
        'q': city_name,
        'appid': API_KEY,
        'units': 'metric',  # 使用摄氏度
        'lang': 'zh_cn'  # 中文描述
    }

    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()  # 检查请求是否成功
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"获取天气数据时出错: {e}")
        return None