from src.weather.api_client import get_weather_data
from src.weather.data_parser import parse_weather_data
from src.weather.multy_city import  get_multiple_city_data, display_cities_comparison
from src.weather.display_utils import clear_screen, print_header, print_success, print_error
from weather.user_preference import UserPreferences
from weather.query_history import QueryHistory

user_prefs = UserPreferences()
query_history = QueryHistory()


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
    print_header("天气预报应用")
    print("1. 查询单个城市天气")
    print("2. 多城市天气对比")
    print("3. 收藏夹管理")
    print("4. 查看查询历史")
    print("5. 退出程序")
    print("="*40)


def single_city_mode():
    """单个城市查询模式"""
    # 显示收藏城市
    favorites = user_prefs.get_favorite_cities()
    if favorites:
        print("\n⭐ 收藏城市:", " | ".join(favorites))

    city = input("\n请输入城市名称: ").strip()
    if not city:
        # 使用默认城市
        city = user_prefs.preferences['default_city']
        print(f"使用默认城市: {city}")

    raw_data = get_weather_data(city)
    weather_info = parse_weather_data(raw_data)

    if 'error' not in weather_info:
        # 记录查询历史
        query_history.add_query(city, weather_info)

        # 询问是否收藏
        if city not in favorites:
            choice = input(f"\n是否将 {city} 添加到收藏夹？(y/N): ").strip().lower()
            if choice in ['y', 'yes', '是']:
                user_prefs.add_favorite_city(city)
                print_success(f"已收藏 {city}")

    display_weather(weather_info)


def favorites_mode():
    """收藏夹管理"""
    print_header("收藏夹管理")

    favorites = user_prefs.get_favorite_cities()

    if not favorites:
        print("暂无收藏城市")
        return

    print("⭐ 收藏城市列表:")
    for i, city in enumerate(favorites, 1):
        print(f"  {i}. {city}")

    print("\n1. 查询收藏城市天气")
    print("2. 移除收藏城市")
    print("3. 返回主菜单")

    choice = input("\n请选择: ").strip()

    if choice == '1':
        # 查询所有收藏城市
        weather_list = get_multiple_city_data(favorites)
        display_cities_comparison(weather_list)
    elif choice == '2':
        city_num = input("请输入要移除的城市编号: ").strip()
        try:
            city_index = int(city_num) - 1
            if 0 <= city_index < len(favorites):
                city_to_remove = favorites[city_index]
                if user_prefs.remove_favorite_city(city_to_remove):
                    print_success(f"已移除 {city_to_remove}")
                else:
                    print_error("移除失败")
            else:
                print_error("无效编号")
        except ValueError:
            print_error("请输入有效数字")


def history_mode():
    """查看查询历史"""
    print_header("查询历史")

    history = query_history.get_recent_queries(20)

    if not history:
        print("暂无查询历史")
        return

    print(f"{'时间':<18} {'城市':<10} {'温度':<8} {'天气':<12}")
    print("-" * 50)

    for record in history:
        print(f"{record['timestamp']:<18} {record['city']:<10} "
              f"{record['temperature']}°C    {record['description']:<12}")

    # 清空历史选项
    if history:
        choice = input("\n是否清空历史记录？(y/N): ").strip().lower()
        if choice in ['y', 'yes', '是']:
            if query_history.clear_history():
                print_success("历史记录已清空")



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
        choice = input("请选择功能 (1-5): ").strip()

        if choice == '1':
            single_city_mode()
        elif choice == '2':
            multi_city_mode()
        elif choice == '3':
            favorites_mode()
        elif choice == '4':
            history_mode()
        elif choice == '5':
            if confirm_exit():
                print_success("感谢使用天气预报应用！再见！👋")
                break
            else:
                continue
        else:
            print_error("无效选择，请输入 1-5")

        input("\n📝 按 Enter 键继续...")
        clear_screen()


if __name__ == "__main__":
    main()