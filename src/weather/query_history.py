import json
import os
from datetime import datetime


class QueryHistory:
    def __init__(self, history_file=None):

        if history_file is None:
            # 获取当前文件的绝对路径
            current_dir = os.path.dirname(os.path.abspath(__file__))
            # 向上两级到 weather-app 目录
            project_root = os.path.dirname(os.path.dirname(current_dir))
            # 构建正确的缓存文件路径
            history_file = os.path.join(project_root, 'data', 'processed', 'query_history.json')

        self.history_file = history_file
        self._ensure_data_dir()
        self.history = self._load_history()

    def _ensure_data_dir(self):
        os.makedirs(os.path.dirname(self.history_file), exist_ok=True)

    def _load_history(self):
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                pass
        return []

    def save_history(self):
        try:
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(self.history, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"保存历史记录失败: {e}")
            return False

    def add_query(self, city, weather_data):
        """添加查询记录"""
        record = {
            'city': city,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'temperature': weather_data.get('temperature', 'N/A'),
            'description': weather_data.get('description', 'N/A')
        }

        # 保留最近50条记录
        self.history.insert(0, record)
        self.history = self.history[:50]

        return self.save_history()

    def get_recent_queries(self, limit=10):
        """获取最近的查询记录"""
        return self.history[:limit]

    def clear_history(self):
        """清空历史记录"""
        self.history = []
        return self.save_history()