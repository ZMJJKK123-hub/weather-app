from src.weather.api_client import get_weather_data
from src.weather.data_parser import parse_weather_data
from src.weather.multy_city import  get_multiple_city_data, display_cities_comparison
from src.weather.display_utils import clear_screen, print_header, print_success, print_error


def display_weather(weather_info):
    """显示天气信息"""
    if not weather_info:
        print("无法获取天气信息")
        return
    print_header(f"{weather_info['city']} 实时天气")

    print(f"{weather_info['icon']}  {weather_info['description']:12} {weather_info['temp_display']:>15}")
    print(f"🤔 体感温度: {weather_info['feels_like']}°C")
    print(f"💧 湿度: {weather_info['humidity']}%")
    print(f"📊 气压: {weather_info['pressure']} hPa")
    print(f"💨 风速: {weather_info['wind_speed']} m/s")

    # 添加舒适度提示
    try:
        temp = float(weather_info['temperature'])
        if temp < 0:
            print("💡 提示: 天气寒冷，注意保暖！")
        elif temp > 30:
            print("💡 提示: 天气炎热，注意防暑！")
    except (ValueError, TypeError):
        pass

def show_welcome():
    """显示欢迎画面"""
    clear_screen()
    print_header("欢迎使用天气预报应用")
    print("✨ 功能特点:")
    print("   • 实时天气查询")
    print("   • 多城市对比")
    print("   • 智能缓存加速")
    print("   • 美观的界面显示")
    print("\n🎯 数据来源: OpenWeatherMap")


def confirm_exit():
    """退出确认"""
    choice = input("\n确定要退出吗？(y/N): ").strip().lower()
    return choice in ['y', 'yes', '是']


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
    show_welcome()



    while True:
        show_menu()
        choice = input("请选择功能 (1-3): ").strip()

        if choice == '1':
            single_city_mode()
        elif choice == '2':
            multi_city_mode()
        elif choice == '3':
            if confirm_exit():
                print_success("感谢使用天气预报应用！再见！👋")
                break
            else:
                continue
        else:
            print("❌ 无效选择，请输入 1-3")

        wait_for_enter()




if __name__ == "__main__":
    main()