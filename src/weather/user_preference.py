import json
import os


class UserPreferences:
    def __init__(self, prefs_file=None):
        # 自动计算正确的缓存文件路径
        if prefs_file is None:
            # 获取当前文件的绝对路径
            current_dir = os.path.dirname(os.path.abspath(__file__))
            # 向上两级到 weather-app 目录
            project_root = os.path.dirname(os.path.dirname(current_dir))
            # 构建正确的缓存文件路径
            prefs_file = os.path.join(project_root, 'data', 'processed', 'user_preferences.json')

        self.prefs_file = prefs_file
        self._ensure_data_dir()
        self.preferences = self._load_preferences()

    def _ensure_data_dir(self):
        """确保数据目录存在"""
        os.makedirs(os.path.dirname(self.prefs_file), exist_ok=True)

    def _load_preferences(self):
        """加载用户偏好设置"""
        if os.path.exists(self.prefs_file):
            try:
                with open(self.prefs_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                print("file not found")


        # 默认设置
        return {
            'favorite_cities': [],
            'default_city': '北京',
            'temperature_unit': 'celsius',
            'theme': 'default'
        }

    def save_preferences(self):
        """保存偏好设置到文件"""
        try:
            with open(self.prefs_file, 'w', encoding='utf-8') as f:
                json.dump(self.preferences, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"保存偏好设置失败: {e}")
            return False

    def add_favorite_city(self, city):
        """添加收藏城市"""
        if city not in self.preferences['favorite_cities']:
            self.preferences['favorite_cities'].append(city)
            return self.save_preferences()
        return True

    def remove_favorite_city(self, city):
        """移除收藏城市"""
        if city in self.preferences['favorite_cities']:
            self.preferences['favorite_cities'].remove(city)
            return self.save_preferences()
        return True

    def get_favorite_cities(self):
        """获取收藏城市列表"""
        return self.preferences['favorite_cities']

    def set_default_city(self, city):
        """设置默认城市"""
        self.preferences['default_city'] = city
        return self.save_preferences()