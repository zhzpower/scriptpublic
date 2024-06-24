import os
import re
import json
import requests
import tglog
import config

try:
    config = __import__("config")
    host = config.host
except:
    host = os.getenv('tg_host')

print(f""" 配置信息：
    tg_host: {host}
    """)

# 解析消息数组，转换为VideoInfoModel数组
def parse_messages(messages: list[str]) -> None:
    tglog.p(f"开始解析，共{len(messages)}条<telegram>消息。。。")
    shows = tv_series_subscription_list()
    tglog.p(f"开始解析，共{len(shows)}条<订阅>消息。。。")

    valid_tv_dicts = {} # tmdbID : tv_dict
    
    for tv in shows:                
        tmdbID = tv["tmdbID"]
        tv_name = tv["name"]
        tglog.p(f"开始查找：{tv_name}")
        if tmdbID is None:
            continue

        for msg in messages:
        # 过滤监听的电视剧
            if msg is not None and tv_name.lower() in msg and ('alipan' in msg or 'aliyundrive' in msg):
                tglog.p("✅✅✅✅找到：", tv_name)
                subscribe_url = get_url_from_msg(msg)
                if subscribe_url is not None:
                    tglog.p(f"✅✅✅✅找到 {tv_name}: {subscribe_url}")
                    tv["subscribeURL"] = subscribe_url
                    valid_tv_dicts[tmdbID] = tv
                    break
                else:
                    tglog.p("解析失败：", tv_name)

        if valid_tv_dicts.get(tmdbID) is None:
            tglog.p("❗️❗️❗️❗️没找到：", tv_name)

    tglog.p(f"过滤后，共有有效消息{len(valid_tv_dicts.values())}条")
    update_tv_subscription_list([tv for tv in valid_tv_dicts.values()])

def get_url_from_msg(msg: str) -> str | None:
    """
    msg:
    名称：**时空线索 (2006) 丹泽尔华盛顿 蓝光原盘REMUX 内封字幕**  

    简介：　　每个人都曾经会被神秘的似曾相识的记忆碎片所困扰过--当你新认识一个人、却觉得在过去曾经遇到过；或者对于一个你从未到过的地方感觉非常熟悉，很多人对此往往就是一笑了之。但是，当这些来自于过去的记忆碎片不断地向你发出对于未来的警示的时候，你又将如何对待这样的情况呢？好莱坞大导演托尼·斯科特携手制片人杰里·布鲁克海莫，一起为观众们打造了一部精彩刺激的惊悚动作电影。　　在片中，道格·卡林(丹泽尔·华盛顿　饰)是一名ATF(美国酒精、烟草与火器管理局)探员，奉命对于一起恐怖袭击案件进行调查。他们所得到的消息是一个名叫奥斯塔特(詹姆斯·卡维泽尔　饰)的极端恐怖分子将要在新奥尔良民用码头安置大威力炸弹，这样，将有数百名平民的生命安全受到威胁。而在这之前，有数起爆炸事件均与奥斯塔特有关。在调查的过程中，卡林遇到一个陌生女人，这个名叫克莱尔的女人向卡林诉说她经常会感觉到一些有关爆炸场面的情景，但是没有人相信她。敏锐的卡林听到这个消息后马上重视起来，他预感到这将是破解这次恐怖袭击的唯一线索……

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
    else:
        print("没有找到链接")
        return None
#     # 调用openAI解析
#     log.p("开始调用openAI: ")
#     json_str = parse_messages_with_openAI(msg_str)
#     json_obj = json.loads(json_str)
#     print(f"解析完成，共{len(json_obj)}条消息。。。")

#     # 转换为VideoInfoModel数组
#     video_info_models = []
#     for obj in json_obj:
#         video_model = VideoInfoModel(obj['id'], obj['name'], obj['episode_name'], obj['subscribe_url'])
#         video_info_models.append(video_model)
#     return video_info_models

# # 解析消息数组，转换为json格式
# def parse_messages_with_openAI(msg_str):
#     print(f"过滤后信息：{msg_str}")

#     response = client.chat.completions.create(
#         model="glm-4v", # glm-4v  kimi
#         messages=[
#             {"role": "user", "content": f'''
#             我是一个数据分析师，可以帮助把给到的数据转换为json格式，消息格式为：{{'id': 1222, 'name': '电视剧名', 'episode_name': '集数名', 'subscribe_url': '集数链接'}}
#             其中，season和episode都是数字，episode_name和subscribe_url是字符串。
#             比如：
#             ```
#             给到的数据为：
#              "   *名称：庆余年2 / 庆余年 第二季 【36集完结】 4K/高码内封字幕 [2024]张若昀/李沁/陈道明**
#                 描述：《庆余年第二季》是由孙皓执导，张若昀、李沁领衔主演，陈道明、吴刚、郭麒麟、田雨、李小冉、宋轶、辛芷蕾、刘端端、付辛博联合主演的古装剧。
#                 该剧根据猫腻的同名小说改编，讲述了一个身世神秘的少年范闲，历经家族、江湖、庙堂的种种考验与锤炼，书写出一段人生传奇的故事。
#                 链接：https://pan.quark.cn/s/c3d041ca7093
#                 ######################
#                 **名称：大象女王 (2019) 4K HDR 中字外挂字幕**
#                 描述：雅典娜是一位母亲，当他们被迫离开他们的水坑时，她会尽她所能保护她的牧群。
#                 链接：https://www.alipan.com/s/ZkDWQFY7qR6
#             "
#             返回格式为：
#             "
#             [{{
#                 "name": "大象女王2019 4K",
#                 "season": 1,
#                 "episode": 1,
#                 "episode_name": "第1集",
#                 "subscribe_url": "https://www.alipan.com/s/ZkDWQFY7qR6"
#             }},{{
#                 "name": "庆余年2",
#                 "season": 2,
#                 "episode": 1,
#                 "episode_name": "第1集",
#                 "subscribe_url": "https://pan.quark.cn/s/c3d041ca7093"
#             }}]
#             "
#             ```
#             那么给到你的信息为：
#             {msg_str}
#             Do not include any explanations, only provide a RFC8259 compliant JSON response following this format without deviation.
#             '''}
#         ],
#         # stream = True,
#         temperature=0,
#         max_tokens=4096,
#         top_p=1,
#         frequency_penalty=0,
#         presence_penalty=0
#     )
#     log.p("解析完成：")
#     res = response.choices[0].message.content

#     res = res.replace("```json\n", "")
#     res = res.replace("```", "")
#     log.p(res)
#     return res

# # 将字符串转换为json格式
# def format_json(my_string):
#     if is_json(my_string):
#         return my_string
#     else:
#         json_str = format_json_with_openAI(my_string)
#         return json_str

# def format_json_with_openAI(my_string):
#     response = client.chat.completions.create(
#         model="glm-4v", # glm-4v  kimi
#         messages=[
#             {"role": "system", "content": '''
#                 我是一个数据分析师，帮助把给到的数据转换为json格式。
#                 Do not include any explanations, only provide a RFC8259 compliant JSON response following this format without deviation.
#                 '''},
#             {"role": "user", "content": my_string}
#         ],
#         # stream = True,
#         temperature=0,
#         max_tokens=4096,
#         top_p=1,
#         frequency_penalty=0,
#         presence_penalty=0
#     )
#     print("格式化完成：")
#     res = response.choices[0].message.content
#     print(res)
#     if is_json(my_string):
#         return my_string
#     else:
#         json_str = format_json_with_openAI(my_string)
#         return json_str
    
# # 判断是否为json格式
# def is_json(my_string):
#     try:
#         json_object = json.loads(my_string)
#     except ValueError as e:
#         return False
#     return True

def tv_series_subscription_list() -> list:
    """
+    从视频数据库API获取TV系列订阅列表。
+
+    返回:
+        list: 一个包含TV系列订阅信息的列表。每个字典包含TV系列名称、流派和发行年份等信息。
+
+    引发:
+        requests.exceptions.RequestException: 如果与API进行HTTP请求时出现错误。
+
+    示例用法:
+        subscriptions = tv_series_subscription_list()
+        for subscription in subscriptions:
+            print(subscription['name'], subscription['tmdbID'], subscription['subscribeURL'])

    """
    url = f"https://{host}/api/shows"
    # url = "http://localhost:8787/api/shows"
    resp = requests.get(url)
    return resp.json()

def update_tv_subscription_list(datas: list):
    tglog.p("开始更新订阅列表")
    # 更新订阅列表
    url = f"https://{host}/api/shows"
    # url = "http://localhost:8787/api/shows"
    resp = requests.put(url, json=json.dumps(datas))
    tglog.p("更新完成：", resp.text)

if __name__ == '__main__':
    shows = tv_series_subscription_list()
    print(shows)