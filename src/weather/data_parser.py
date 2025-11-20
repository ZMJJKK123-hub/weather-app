from src.weather.display_utils import *

def parse_weather_data(weather_data):
    """解析天气数据，包含错误检查"""
    if isinstance(weather_data, dict) and 'error' in weather_data:
        return weather_data

    if not weather_data:
        return {'error': '无天气数据返回'}

    try:
        main_data = weather_data['main']
        weather_info = weather_data['weather'][0]

        description = weather_info.get('description', 'N/A')
        temperature = main_data.get('temp', 'N/A')

        return {
            'city': weather_data.get('name', '未知城市'),
            'temperature': temperature,
            'feels_like': main_data.get('feels_like', 'N/A'),
            'humidity': main_data.get('humidity', 'N/A'),
            'pressure': main_data.get('pressure', 'N/A'),
            'description': description,
            'wind_speed': weather_data.get('wind', {}).get('speed', 'N/A'),
            'icon': print_weather_icon(description),
            'temp_display': format_temperature(temperature)
        }
    except (KeyError, IndexError, TypeError) as e:
        return {'error': f'数据解析失败: {str(e)}'}