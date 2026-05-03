"""
Week 5 Day 5 - Round 3: 双模型AI客户端
支持 DeepSeek 和 智谱AI 自由切换
核心思想：两个模型底层都是requests发HTTP，只是URL、Key、模型名不同
"""
import requests
import os
from dotenv import load_dotenv

load_dotenv()


class DualAIClient:
    """双模型AI客户端，支持DeepSeek和智谱AI切换"""

    def __init__(self, model="deepseek", system_prompt="你是一个Python老师"):
        """
        初始化
        :param model: 'deepseek' 或 'zhipu'
        :param system_prompt: 系统提示词，设定AI角色
        """
        self.model = model
        self.system_prompt = system_prompt
        # 历史消息，初始化时放入system角色
        self.history = [{"role": "system", "content": system_prompt}]

        # 两个模型的配置（URL、Key、模型名）
        # 核心：只有这三个值不同，其他代码完全一样
        self.configs = {
            "deepseek": {
                "url": "https://api.deepseek.com/v1/chat/completions",
                "key": os.getenv("DEEPSEEK_API_KEY"),
                "model": "deepseek-chat"
            },
            "zhipu": {
                "url": "https://open.bigmodel.cn/api/paas/v4/chat/completions",
                "key": os.getenv("ZHIPUAI_API_KEY"),
                "model": "glm-4-flash"
            }
        }

    def _call_api(self):
        """
        统一的API调用方法
        两个模型共用这一套代码，因为requests调用方式完全一样
        只是URL、Key、模型名从config里取不同的值
        """
        # 根据当前模型取对应配置
        config = self.configs[self.model]

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {config['key']}"
        }
        data = {
            "model": config["model"],
            "messages": self.history    # 每次发完整history
        }

        response = requests.post(config["url"], headers=headers, json=data)
        result = response.json()

        # 取AI回复（两个模型返回的都是字典，取法一样）
        return result['choices'][0]['message']['content']

    def ask(self, question):
        """
        发消息给AI
        1. 用户消息加入history
        2. 调用API
        3. AI回复加入history
        4. 返回回复
        """
        # 加用户消息到历史
        self.history.append({"role": "user", "content": question})

        try:
            # 调用API（内部自动判断用哪个模型）
            reply = self._call_api()
        except Exception as e:
            # 请求失败时，把刚才加的用户消息撤掉，保持history干净
            self.history.pop()
            return f"请求失败: {e}"

        # 加AI回复到历史
        self.history.append({"role": "assistant", "content": reply})
        return reply

    def switch_model(self, model):
        """
        切换模型
        :param model: 'deepseek' 或 'zhipu'
        注意：历史保留！切换模型不影响之前的对话
        """
        if model not in self.configs:
            print(f"不支持的模型: {model}，可选: {list(self.configs.keys())}")
            return
        self.model = model
        print(f"已切换到: {model}")

    def reset(self):
        """清空对话历史，只保留system prompt"""
        self.history = [{"role": "system", "content": self.system_prompt}]
        print("历史已清空")

    def show_history(self):
        """显示对话历史（跳过system消息）"""
        print("\n--- 对话历史 ---")
        for msg in self.history:
            if msg["role"] == "system":
                continue
            # user消息用"你："，assistant消息用"AI："
            prefix = "你：" if msg["role"] == "user" else "AI："
            print(f"{prefix}{msg['content']}")
        print(f"（共 {len(self.history)} 条消息，含system）")


# ========== 测试 ==========
if __name__ == "__main__":
    # 创建客户端，默认用DeepSeek
    client = DualAIClient(model="deepseek")

    print("=== 双模型AI客户端 ===")
    print("命令: switch (切换模型) | reset (清空历史) | history (查看历史) | quit (退出)")
    print(f"当前模型: {client.model}")

    while True:
        user_input = input("\n你：")

        if user_input.lower() == 'quit':
            break
        elif user_input.lower() == 'switch':
            # 在两个模型之间切换
            new_model = "zhipu" if client.model == "deepseek" else "deepseek"
            client.switch_model(new_model)
            continue
        elif user_input.lower() == 'reset':
            client.reset()
            continue
        elif user_input.lower() == 'history':
            client.show_history()
            continue

        # 正常对话
        reply = client.ask(user_input)
        print(f"AI：{reply}")
