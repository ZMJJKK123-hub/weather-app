import requests
from config.settings import API_KEY, BASE_URL


def get_weather_data(city_name):
    """获取城市天气数据"""

    if not city_name or not city_name.strip():
        return {'error': '城市名称不能为空'}


    params = {
        'q': city_name,
        'appid': API_KEY,
        'units': 'metric',  # 使用摄氏度
        'lang': 'zh_cn'  # 中文描述
    }

    try:
        response = requests.get(BASE_URL, params=params, timeout=10)

        # 处理不同的HTTP状态码
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 401:
            return {'error': 'API密钥无效，请检查配置'}
        elif response.status_code == 404:
            return {'error': f'找不到城市: {city_name}'}
        elif response.status_code == 429:
            return {'error': 'API调用次数超限，请稍后重试'}
        else:
            return {'error': f'API请求失败，状态码: {response.status_code}'}

    except requests.exceptions.Timeout:
        return {'error': '请求超时，请检查网络连接'}
    except requests.exceptions.ConnectionError:
        return {'error': '网络连接错误，请检查网络设置'}
    except requests.exceptions.RequestException as e:
        return {'error': f'网络请求异常: {str(e)}'}
    except Exception as e:
        return {'error': f'未知错误: {str(e)}'}