import requests
import os
from dotenv import load_dotenv

load_dotenv()


class AIClient:
    """双模型AI客户端，支持DeepSeek和智谱AI"""

    CONFIGS = {
        'deepseek': {
            'url': 'https://api.deepseek.com/v1/chat/completions',
            'key': os.getenv('DEEPSEEK_API_KEY'),
            'model': 'deepseek-chat',
        },
        'zhipu': {
            'url': 'https://open.bigmodel.cn/api/paas/v4/chat/completions',
            'key': os.getenv('ZHIPU_API_KEY'),
            'model': 'glm-4-flash',
        },
    }

    def __init__(self, model='deepseek', system_prompt='你是一个有用的AI助手。'):
        if model not in self.CONFIGS:
            raise ValueError(f"不支持的模型: {model}，可选: {list(self.CONFIGS.keys())}")
        self.model = model
        self.system_prompt = system_prompt
        self.history = []  # 内存中的对话历史（从数据库加载后在这里）

    def _call_api(self, messages):
        """统一API调用方法"""
        config = self.CONFIGS[self.model]
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f"Bearer {config['key']}",
        }
        data = {
            'model': config['model'],
            'messages': messages,
        }
        response = requests.post(config['url'], headers=headers, json=data, timeout=30)
        response.raise_for_status()
        return response.json()['choices'][0]['message']['content']

    def ask(self, user_message):
        """发送消息并获取回复"""
        # 1. 加用户消息到历史
        self.history.append({'role': 'user', 'content': user_message})

        # 2. 构建完整消息列表：system + 历史
        messages = [{'role': 'system', 'content': self.system_prompt}] + self.history

        try:
            # 3. 调用API
            reply = self._call_api(messages)
            # 4. 加AI回复到历史
            self.history.append({'role': 'assistant', 'content': reply})
            return reply
        except Exception as e:
            # 5. 失败时移除刚才的用户消息，保持历史干净
            self.history.pop()
            raise e

    def load_history(self, history_list):
        """从数据库加载历史记录"""
        self.history = history_list

    def reset(self):
        """清空对话历史"""
        self.history = []
