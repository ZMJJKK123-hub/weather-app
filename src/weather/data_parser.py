def parse_weather_data(weather_data):
    """解析天气数据，提取关键信息"""
    if not weather_data:
        return None

    main_data = weather_data['main']
    weather_info = weather_data['weather'][0]

    return {
        'city': weather_data['name'],
        'temperature': main_data['temp'],
        'feels_like': main_data['feels_like'],
        'humidity': main_data['humidity'],
        'pressure': main_data['pressure'],
        'description': weather_info['description'],
        'wind_speed': weather_data['wind']['speed']
    }