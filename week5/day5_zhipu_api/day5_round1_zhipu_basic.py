"""
Week 5 Day 5 - Round 1: 智谱AI基础调用（用requests方式，不依赖zhipuai SDK）
"""
import requests
import os
from dotenv import load_dotenv

# 加载 .env 里的 API Key
load_dotenv()

# 智谱AI的接口地址（和DeepSeek一样是标准HTTP接口）
url = "https://open.bigmodel.cn/api/paas/v4/chat/completions"

# 请求头：JSON格式 + Bearer Token认证
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {os.getenv('ZHIPUAI_API_KEY')}"
}

# 请求体：和DeepSeek格式完全一样
data = {
    "model": "glm-4-flash",           # 智谱的模型名（DeepSeek用的是deepseek-chat）
    "messages": [
        {"role": "system", "content": "你是一个Python老师，用简洁的语言回答"},
        {"role": "user", "content": "Python的装饰器是什么？用一句话解释"}
    ]
}

# 发POST请求
response = requests.post(url, headers=headers, json=data)

# 取回复（和DeepSeek一模一样的取法，因为都是字典）
reply = response.json()['choices'][0]['message']['content']
print("AI回复：", reply)

# 查看完整响应结构
print("\n--- 完整响应 ---")
result = response.json()
print(f"模型: {result.get('model', '未知')}")
print(f"token用量: {result.get('usage', '未知')}")
