"""
工具类
"""

def load_config():
    """加载配置信息"""
    config = None
    try:
        config = __import__("config")
    except ImportError:
        print("config.py 文件不存在，请检查配置！")
    return config
