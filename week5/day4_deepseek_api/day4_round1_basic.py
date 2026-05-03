# day4_round1_basic.py
# Week 5 Day 4 - Round 1: 用 requests 库调用 DeepSeek API（最底层，理解原理）

import os
import requests
from dotenv import load_dotenv

# ① 从 .env 文件读取 API Key（绝不能硬编码！）
load_dotenv()
API_KEY = os.getenv("DEEPSEEK_API_KEY")

# ② DeepSeek API 地址
URL = "https://api.deepseek.com/v1/chat/completions"

# ③ 请求头：Bearer Token 认证 + JSON 格式
headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# ④ 请求体：告诉AI用什么模型、发什么消息
data = {
    "model": "deepseek-chat",
    "messages": [
        {"role": "user", "content": "用一句话介绍你自己"}
    ]
}

# ⑤ 发送 POST 请求
print("正在请求 DeepSeek API...")
response = requests.post(URL, headers=headers, json=data)

# ⑥ 检查响应状态
if response.status_code == 200:
    result = response.json()
    # ⑦ 从响应中提取AI回复
    reply = result['choices'][0]['message']['content']
    print(f"\nAI回复：{reply}")
else:
    print(f"请求失败，状态码：{response.status_code}")
    print(f"错误信息：{response.text}")
