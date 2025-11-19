def parse_weather_data(weather_data):
    """解析天气数据，提取关键信息"""
    if isinstance(weather_data, dict) and 'error' in weather_data:
        return weather_data

    if not weather_data:
        return {'error': '无天气数据返回'}

    try:
        # 检查必要字段是否存在
        if 'main' not in weather_data or 'weather' not in weather_data:
            return {'error': '返回数据格式不正确'}

        main_data = weather_data['main']
        weather_info = weather_data['weather'][0]

        # 提取数据，提供默认值防止KeyError
        return {
            'city': weather_data.get('name', '未知城市'),
            'temperature': main_data.get('temp', 'N/A'),
            'feels_like': main_data.get('feels_like', 'N/A'),
            'humidity': main_data.get('humidity', 'N/A'),
            'pressure': main_data.get('pressure', 'N/A'),
            'description': weather_info.get('description', 'N/A'),
            'wind_speed': weather_data.get('wind', {}).get('speed', 'N/A')
        }
    except (KeyError, IndexError, TypeError) as e:
        return {'error': f'数据解析失败: {str(e)}'}