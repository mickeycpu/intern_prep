"""
Week 5 Day 5 - Round 2: 智谱AI多轮对话（用requests方式）
和DeepSeek多轮对话代码几乎一样，只是URL、Key、模型名不同
"""
import requests
import os
from dotenv import load_dotenv

load_dotenv()

# 智谱AI配置（对比DeepSeek：只改了这三行）
url = "https://open.bigmodel.cn/api/paas/v4/chat/completions"
api_key = os.getenv("ZHIPUAI_API_KEY")
model = "glm-4-flash"

# 历史消息列表（和DeepSeek一样，每次发完整history）
history = [
    {"role": "system", "content": "你是一个Python老师"}
]

print("=== 智谱AI多轮对话（输入 quit 退出）===")

while True:
    user_input = input("\n你：")
    if user_input.lower() == 'quit':
        break

    # 把用户消息加入历史
    history.append({"role": "user", "content": user_input})

    # 发请求（每次把完整history发过去）
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    data = {
        "model": model,
        "messages": history      # 完整历史，AI靠这个"记住"上下文
    }

    response = requests.post(url, headers=headers, json=data)
    result = response.json()

    # 取AI回复
    reply = result['choices'][0]['message']['content']

    # 把AI回复也加入历史（下次发请求时AI能看到自己说过的话）
    history.append({"role": "assistant", "content": reply})

    print(f"AI：{reply}")
    print(f"[历史消息数: {len(history)}]")
