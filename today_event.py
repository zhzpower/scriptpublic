#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
import os
from openai import OpenAI
import requests
# from config import APIKEY, BASEURL, ACCESSTOKEN

APIKEY = os.getenv('APIKEY')
BASEURL = os.getenv('BASEURL')
ACCESSTOKEN = os.getenv('ACCESSTOKEN')

client = OpenAI(
    api_key = APIKEY,
    base_url = BASEURL,
)

print("#############################开始获取今天事件， 使用模式：metaso 研究搜索")
response = client.chat.completions.create(
    model = "metaso", #
    messages = [
        {"role": "user", "content": """
        研究搜索：今天发生的国内外经济和军事大事件. 请用markdown格式输出, 分别输出今天发生的国内外经济和军事大事件。
        军事方面重点关注中国、俄罗斯、美国、乌克兰、新加坡、澳大利亚、日本、欧洲、中东等方面的消息。
        """
        }
    ],
    # stream = True,
    temperature = 0,
    max_tokens = 4096,
    top_p = 1,
    frequency_penalty = 0,
    presence_penalty = 0
)

content = response.choices[0].message.content
print(content)

print("\n\n#############################获取今天事件完成， 开始发送钉钉消息")
# 通过webhook发送钉钉日报
webhook_url = f"https://oapi.dingtalk.com/robot/send?access_token={ACCESSTOKEN}"
message = {
    "msgtype": "markdown",
    "markdown": {
        "title": "今天发生的国内外大事件",
        "text": content
    }
}
response = requests.post(webhook_url, json=message)
print("发送结果：", response.text)