# day4_round3_oop.py
# Week 5 Day 4 - Round 3: 封装成 DeepSeekClient 类（OOP风格，项目中用这种）

import os
import requests
from dotenv import load_dotenv

load_dotenv()


class DeepSeekClient:
    """DeepSeek API 封装类"""

    def __init__(self, api_key=None, system_prompt="你是一个有用的助手"):
        self.api_key = api_key or os.getenv("DEEPSEEK_API_KEY")
        self.url = "https://api.deepseek.com/v1/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        self.system_prompt = system_prompt
        self.history = []
        self._init_history()

    def _init_history(self):
        """初始化对话历史，加入system角色"""
        if self.system_prompt:
            self.history = [{"role": "system", "content": self.system_prompt}]

    def ask(self, question):
        """发送一个问题，返回AI回复"""
        self.history.append({"role": "user", "content": question})

        data = {
            "model": "deepseek-chat",
            "messages": self.history
        }

        response = requests.post(self.url, headers=self.headers, json=data)

        if response.status_code == 200:
            reply = response.json()['choices'][0]['message']['content']
            self.history.append({"role": "assistant", "content": reply})
            return reply
        else:
            error_msg = f"[错误 {response.status_code}] {response.text}"
            # 请求失败，移除刚才加的用户消息
            self.history.pop()
            return error_msg

    def reset(self):
        """清空对话历史，重新开始"""
        self._init_history()
        print("对话已重置")

    def get_history(self):
        """获取对话历史"""
        return self.history

    def show_history(self):
        """打印对话历史（可读格式）"""
        for msg in self.history:
            role = msg['role']
            content = msg['content']
            if role == 'system':
                print(f"[系统] {content}")
            elif role == 'user':
                print(f"[你] {content}")
            elif role == 'assistant':
                print(f"[AI] {content}")
            print()


# ===== 使用示例 =====
if __name__ == '__main__':
    # 创建客户端，设定AI角色
    client = DeepSeekClient(
        system_prompt="你是一个Python面试官，先问问题，等回答后再给评价和参考答案"
    )

    # 第一轮
    print("--- 第一轮 ---")
    reply1 = client.ask("请给我一道Python装饰器的面试题")
    print(f"AI：{reply1}")

    # 第二轮（AI记住上下文，知道自己是面试官）
    print("\n--- 第二轮 ---")
    reply2 = client.ask("装饰器就是在不修改原函数代码的情况下，给函数添加新功能。用@语法糖放在函数定义前面。")
    print(f"AI：{reply2}")

    # 查看对话历史
    print("\n--- 对话历史 ---")
    client.show_history()

    # 重置对话
    client.reset()

    # 新话题
    print("\n--- 重置后 ---")
    reply3 = client.ask("什么是RESTful API？")
    print(f"AI：{reply3}")
