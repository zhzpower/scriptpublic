"""
任务名称
name: 订阅TG频道中阿里云盘的 电视剧
定时规则
cron: 1 9 * * *
"""

import os
from telethon import TelegramClient
from telethon.errors.rpcerrorlist import AuthKeyError
from telethon.sync import TelegramClient as SyncTelegramClient
from telethon.sessions import StringSession
from .tgparser import parse_messages
from .tglog import a
from .tgutils import load_config

a("获取TG的历史消息中...")
CONFIG = load_config()
if CONFIG is not None:
    session_name = CONFIG.session_name
    api_id = CONFIG.api_id
    api_hash = CONFIG.api_hash
    tg_channels = CONFIG.tg_channels
    session_string = CONFIG.session_string
else:
    session_name = os.getenv('tg_session_name')
    api_id = os.getenv('tg_api_id')
    api_hash = os.getenv('tg_api_hash')
    tg_channels = os.getenv('tg_tg_channels')
    session_string = os.getenv('tg_session_string')

print(f""" 配置信息：
    tg_channels：{tg_channels}
    session_name：{session_name}
    api_id：{api_id}
    api_hash：{api_hash}
    tg_session_string：{session_string}
    """)

# with TelegramClient(StringSession(), api_id, api_hash) as client:
#     print(client.session.save())

try:
    # client = TelegramClient(session_name, api_id, api_hash, proxy=proxy)
    proxy = ('http', '192.168.50.120', 7890)
    # proxy = ()
    client = TelegramClient(StringSession(session_string), api_id, api_hash, proxy=proxy)
    client.start() # client.connect()
except AuthKeyError:
    client = SyncTelegramClient(session_name, api_id, api_hash)
    client.start()

# 群组的用户名或ID；Quark_Share_Channel
total_messages: list[list[str]] = []
MAX_LEN = 0
for channel in tg_channels.split(','):
    # 获取群组实体
    group_entity = client.get_entity(channel)
    # 获取历史消息
    messages = client.get_messages(group_entity, limit=200)  # 获取最新的50条消息
    # 获取参考消息之后的消息
    # messages = client.get_messages(group_entity, min_id=39309)
    total_messages.append(messages)
    MAX_LEN = max(MAX_LEN, len(messages))
# 关闭连接
client.disconnect()
a(f"共获取到 {len(messages)} 条TG的历史消息")

# 打印消息
pengding_messages: list[str] = []
for i in range(MAX_LEN):
    for messages in total_messages:
        if i < len(messages):
            message = messages[i]
            # print(message.text)
            pengding_messages.append(message.text)

a("1、开始解析消息，获取订阅的电视剧网盘地址")
parse_messages(pengding_messages)
# a(f"  获取到有效的网盘地址")

# a("2、开始获取每集的下载地址")
# ds: list[DownloadsInfo] = tgyunpan.get_all_files_download_url(subscribe_list)
# tgdownloads.downloads(ds)

# a("3、开始获取下载")
