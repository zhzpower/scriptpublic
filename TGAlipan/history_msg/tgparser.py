"""
解析TG消息，获取电视剧订阅列表，更新到cloud中
"""
import os
import re
import json
import requests
from tglog import p
from tgutils import load_config

CONFIG = load_config()
if CONFIG is not None:
    host = CONFIG.host
else:
    host = os.getenv('tg_host')

print(f""" 配置信息：
    tg_host: {host}
    """)

def parse_messages(messages: list[str]) -> None:
    """
    解析消息数组，转换为数组
    """
    p(f"开始解析，共{len(messages)}条<telegram>消息。。。")
    shows = tv_series_subscription_list()
    p(f"订阅的数据：{shows}")
    p(f"开始解析，共{len(shows)}条<订阅>消息。。。")

    valid_tv_dicts = {} # tmdbID : tv_dict

    for tv in shows:
        tmdb_id = tv["tmdbID"]
        tv_name = tv["name"]
        p(f"开始查找：{tv_name}")
        if tmdb_id is None:
            continue

        for msg in messages:
        # 过滤监听的电视剧
            if tv_name is None and tv_name.lower() in msg and ('alipan' in msg or 'aliyundrive' in msg):
                p("✅✅✅✅找到：", tv_name)
                subscribe_url = get_url_from_msg(msg)
                if subscribe_url is not None:
                    p(f"✅✅✅✅找到 {tv_name}: {subscribe_url}")
                    tv["subscribeURL"] = subscribe_url
                    valid_tv_dicts[tmdb_id] = tv
                    break
                p("解析失败：", tv_name)

        if valid_tv_dicts.get(tmdb_id) is None:
            p("❗️❗️❗️❗️没找到：", tv_name)

    p(f"过滤后，共有有效消息{len(valid_tv_dicts.values())}条")
    update_tv_subscription_list(list(valid_tv_dicts.values()))

def get_url_from_msg(msg: str) -> str | None:
    """
    msg:
    名称：**时空线索 (2006) 丹泽尔华盛顿 蓝光原盘REMUX 内封字幕**  

    简介：　　每个人都曾经会被神秘的似曾相识的记忆碎片所困扰过--当你新认识一个人、却觉得在过去曾经遇到过；
            或者对于一个你从未到过的地方感觉非常熟悉，很多人对此往往就是一笑了之。

    标签：#时空线索 #动作 #惊悚 #科幻 #REMUX  
    大小：23G

    链接：
    [https://www.alipan.com/s/YeZTpTNF11p](https://www.alipan.com/s/YeZTpTNF11p)  

    output:
    https://www.alipan.com/s/YeZTpTNF11p
    """

    # 使用正则表达式提取链接
    pattern = r"https://www\.(?:alipan|aliyundrive)\.com/s/\w+"
    matches = re.findall(pattern, msg)

    if matches:
        for link in matches:
            print("找到的链接:", link)
        return matches.pop(0)

    print("没有找到链接")
    return None

def tv_series_subscription_list() -> list:
    """
+    从视频数据库API获取TV系列订阅列表。
+    返回:
+        list: 一个包含TV系列订阅信息的列表。每个字典包含TV系列名称、流派和发行年份等信息。
+    示例用法:
+        subscriptions = tv_series_subscription_list()
+        for subscription in subscriptions:
+            print(subscription['name'], subscription['tmdbID'], subscription['subscribeURL'])
    """
    url = f"https://{host}/api/shows"
    # url = "http://localhost:8787/api/shows"
    resp = requests.get(url, timeout=15)
    return resp.json()

def update_tv_subscription_list(datas: list):
    """
    更新订阅列表
    """
    p("开始更新订阅列表")
    # 更新订阅列表
    url = f"https://{host}/api/shows"
    # url = "http://localhost:8787/api/shows"
    resp = requests.put(url, json=json.dumps(datas), timeout=15)
    p("更新完成：", resp.text)

if __name__ == '__main__':
    temp_shows = tv_series_subscription_list()
    print(temp_shows)
