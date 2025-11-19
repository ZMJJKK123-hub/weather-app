from src.weather.api_client import get_weather_data
from src.weather.data_parser import parse_weather_data


def display_weather(weather_info):
    """显示天气信息"""
    if not weather_info:
        print("无法获取天气信息")
        return

    print(f"\n=== {weather_info['city']} 天气 ===")
    print(f"温度: {weather_info['temperature']}°C")
    print(f"体感温度: {weather_info['feels_like']}°C")
    print(f"天气: {weather_info['description']}")
    print(f"湿度: {weather_info['humidity']}%")
    print(f"气压: {weather_info['pressure']} hPa")
    print(f"风速: {weather_info['wind_speed']} m/s")


def main():
    print("=== 天气预报应用 ===")

    while True:
        city = input("\n请输入城市名称 (输入 'quit' 退出): ").strip()

        if city.lower() == 'quit':
            break

        if not city:
            print("城市名称不能为空")
            continue

        # 获取并显示天气数据
        raw_data = get_weather_data(city)
        weather_info = parse_weather_data(raw_data)
        display_weather(weather_info)


if __name__ == "__main__":
    main()