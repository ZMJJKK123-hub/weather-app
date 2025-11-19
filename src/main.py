from src.weather.api_client import get_weather_data
from src.weather.data_parser import parse_weather_data
from src.weather.multy_city import  get_multiple_city_data, display_cities_comparison
import time


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

def show_menu():
    """显示主菜单"""
    print("\n" + "="*40)
    print("🌤️  天气预报应用")
    print("="*40)
    print("1. 查询单个城市天气")
    print("2. 多城市天气对比")
    print("3. 退出程序")
    print("="*40)


def single_city_mode():
    """单个城市查询模式"""
    city = input("请输入城市名称: ").strip()
    if not city:
        print("❌ 城市名称不能为空")
        return

    raw_data = get_weather_data(city)
    weather_info = parse_weather_data(raw_data)
    display_weather(weather_info)


def multi_city_mode():
    """多城市对比模式"""
    cities_input = input("请输入城市名称，用逗号分隔 (例如: 北京,上海,广州): ").strip()
    if not cities_input:
        print("❌ 请输入至少一个城市名称")
        return

    city_list = [city.strip() for city in cities_input.split(',') if city.strip()]

    if not city_list:
        print("❌ 没有有效的城市名称")
        return

    weather_list = get_multiple_city_data(city_list)
    display_cities_comparison(weather_list)

def wait_for_enter():
    input("\n按 Enter 键继续...")

def main():
    print("=== 天气预报应用 ===")



    while True:
        show_menu()
        choice = input("请选择功能 (1-3): ").strip()

        if choice == '1':
            single_city_mode()
        elif choice == '2':
            multi_city_mode()
        elif choice == '3':
            print("👋 感谢使用天气预报应用！")
            break
        else:
            print("❌ 无效选择，请输入 1-3")

        wait_for_enter()




if __name__ == "__main__":
    main()