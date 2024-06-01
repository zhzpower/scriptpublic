from openai import OpenAI


client = OpenAI(
    api_key="",
    base_url="https://api.deepseek.com",
)

response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[
        {"role": "system", "content": "你是一个助手"},
        {"role": "user", "content": "使用RxSwift写一个列表页面"}
    ],
    # stream = True,
    temperature=0,
    max_tokens=4096,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
)

print(response.choices[0].message.content)