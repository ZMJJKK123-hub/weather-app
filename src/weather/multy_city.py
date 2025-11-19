from src.weather import api_client,data_parser

def get_multiple_city_data(city_list):
    #获取多个城市数据
    results=[]

    for city in city_list:
        print(f"正在获取 {city} 的天气...")
        raw_data = api_client.get_weather_data(city)
        weather_info = data_parser.parse_weather_data(raw_data)
        results.append(weather_info)

    return results


def display_cities_comparison(weather_list):
    """并排显示多个城市天气对比"""
    print("\n" + "=" * 80)
    print("🏙️  多城市天气对比")
    print("=" * 80)

    # 表头
    headers = ["城市", "温度", "天气", "湿度", "风速"]
    print(f"{headers[0]:<10} {headers[1]:<8} {headers[2]:<12} {headers[3]:<6} {headers[4]:<8}")
    print("-" * 50)

    for weather in weather_list:
        if 'error' in weather:
            print(f"❌ {weather['city']}: {weather['error']}")
        else:
            print(f"🌍 {weather['city']:<8} {weather['temperature']}°C    "
                  f"{weather['description']:<10} {weather['humidity']}%     "
                  f"{weather['wind_speed']}m/s")