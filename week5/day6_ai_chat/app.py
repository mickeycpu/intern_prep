from flask import Flask
from chat import bp as chat_bp

app = Flask(__name__)
app.secret_key = 'ai_chat_secret_key'

# 注册蓝图
app.register_blueprint(chat_bp)


@app.route('/')
def index():
    return {
        'code': 200,
        'message': 'AI Chat API 服务运行中',
        'endpoints': {
            'POST /api/chat': '发送消息',
            'GET /api/chat/history?session_id=xxx': '查看历史',
        }
    }


if __name__ == '__main__':
    app.run(debug=True, port=5000)
