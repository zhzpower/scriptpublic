"""
相关的class定义

"""

import enum

# 模块
class TGModule(enum.Enum):
    """
    模块名称
    """
    TG_API_MSG   = "TG_API_MSG  "       # 收到消息
    TG_PARSE     = "TG_PARSE_MSG"     # 解析消息
    TG_SUBSCRIBE = "TG_SUBSCRIBE"     # 阿里云订阅
    TG_DOWNLOAD  = "TG_DOWNLOAD "      # 下载文件
