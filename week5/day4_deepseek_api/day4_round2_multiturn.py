# day4_round2_multiturn.py
# Week 5 Day 4 - Round 2: 多轮对话（AI能记住上下文）+ system角色设定

import os
import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("DEEPSEEK_API_KEY")
URL = "https://api.deepseek.com/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}


def chat(messages):
    """发送对话请求，返回AI回复"""
    data = {
        "model": "deepseek-chat",
        "messages": messages
    }
    response = requests.post(URL, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content']
    else:
        return f"[错误 {response.status_code}] {response.text}"


# --- 演示1：system角色设定AI人设 ---
print("=" * 50)
print("演示1：system角色")
print("=" * 50)

messages_with_system = [
    {"role": "system", "content": "你是一个严格的Python老师，回答要简洁，用中文，每次回答不超过3句话"},
    {"role": "user", "content": "什么是装饰器？"}
]

reply = chat(messages_with_system)
print(f"AI（老师人设）：{reply}")


# --- 演示2：多轮对话（AI记住上下文）---
print("\n" + "=" * 50)
print("演示2：多轮对话")
print("=" * 50)

messages_multi = [
    {"role": "system", "content": "你是一个友好的助手"},
    {"role": "user", "content": "我叫张添宇，我在武汉学Python"},
    {"role": "assistant", "content": "你好张添宇！武汉是个好城市，学Python也很有前途，加油！"},
    {"role": "user", "content": "你还记得我叫什么吗？我在哪个城市？"}
]

reply2 = chat(messages_multi)
print(f"AI回复：{reply2}")


# --- 演示3：循环对话（实时聊天）---
print("\n" + "=" * 50)
print("演示3：实时聊天（输入quit退出）")
print("=" * 50)

chat_history = [
    {"role": "system", "content": "你是一个Python学习助手，帮助用户解答Python相关问题，回答简洁明了"}
]

while True:
    user_input = input("\n你：").strip()
    if user_input.lower() in ('quit', 'exit', 'q'):
        print("退出聊天")
        break
    if not user_input:
        continue

    # 把用户消息加入历史
    chat_history.append({"role": "user", "content": user_input})

    # 发送整个对话历史（AI才能记住上下文）
    ai_reply = chat(chat_history)
    print(f"AI：{ai_reply}")

    # 把AI回复也加入历史
    chat_history.append({"role": "assistant", "content": ai_reply})
