import os
import sys

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header(title):
    """打印彩色标题"""
    print(f"\n{'='*50}")
    print(f"🌤️  {title}")
    print(f"{'='*50}")


def print_success(message):
    """打印成功消息"""
    print(f"✅ {message}")


def print_error(message):
    """打印错误消息"""
    print(f"❌ {message}")


def print_warning(message):
    """打印警告消息"""
    print(f"⚠️  {message}")


def print_weather_icon(description):
    """根据天气描述返回对应的图标"""
    icon_map = {
        '晴': '☀️', '多云': '⛅', '阴': '☁️', '雨': '🌧️',
        '雪': '❄️', '雷': '⛈️', '雾': '🌫️', '风': '💨'
    }

    for key, icon in icon_map.items():
        if key in description:
            return icon
    return '🌡️'


def format_temperature(temp):
    """格式化温度显示，添加颜色提示"""
    try:
        temp_value = float(temp)
        if temp_value < 0:
            return f"❄️ {temp}°C"  # 寒冷
        elif temp_value < 10:
            return f"🥶 {temp}°C"  # 冷
        elif temp_value < 25:
            return f"😊 {temp}°C"  # 舒适
        else:
            return f"🥵 {temp}°C"  # 热
    except (ValueError, TypeError):
        return f"{temp}°C"