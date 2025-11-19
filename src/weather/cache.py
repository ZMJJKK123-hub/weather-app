import time
import os
import json


class WeatherCache:
    def __init__(self, cache_file=None, ttl=600):
        # 自动计算正确的缓存文件路径
        if cache_file is None:
            # 获取当前文件的绝对路径
            current_dir = os.path.dirname(os.path.abspath(__file__))
            # 向上两级到 weather-app 目录
            project_root = os.path.dirname(os.path.dirname(current_dir))
            # 构建正确的缓存文件路径
            cache_file = os.path.join(project_root, 'data', 'processed', 'weather_cache.json')

        self.cache_file = cache_file
        self.ttl = ttl
        self._ensure_cache_dir()

    def _ensure_cache_dir(self):
        """确保缓存目录存在"""
        os.makedirs(os.path.dirname(self.cache_file), exist_ok=True)

    def get(self, city):
        """从缓存获取数据"""
        if not os.path.exists(self.cache_file):
            return None

        try:
            with open(self.cache_file, 'r', encoding='utf-8') as f:
                cache = json.load(f)

            if city in cache:
                data, timestamp = cache[city]
                if time.time() - timestamp < self.ttl:
                    return data
        except (json.JSONDecodeError, KeyError, ValueError):
            pass

        return None

    def set(self, city, data):
        """保存数据到缓存"""
        try:
            # 读取现有缓存
            if os.path.exists(self.cache_file):
                with open(self.cache_file, 'r', encoding='utf-8') as f:
                    cache = json.load(f)
            else:
                cache = {}

            # 更新缓存
            cache[city] = (data, time.time())

            # 写入文件
            with open(self.cache_file, 'w', encoding='utf-8') as f:
                json.dump(cache, f, ensure_ascii=False, indent=2)

        except Exception as e:
            print(f"缓存保存失败: {e}")