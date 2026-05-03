import uuid
from flask import Blueprint, request, jsonify
from db import get_db
from ai_client import AIClient

bp = Blueprint('chat', __name__, url_prefix='/api/chat')


def save_message(session_id, role, content):
    """把一条消息存入数据库"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO chat_history (session_id, role, content) VALUES (%s, %s, %s)",
        (session_id, role, content)
    )
    conn.commit()
    cursor.close()
    conn.close()


def load_history(session_id):
    """从数据库加载某个会话的全部历史"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT role, content FROM chat_history WHERE session_id = %s ORDER BY id ASC",
        (session_id,)
    )
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return [{'role': row['role'], 'content': row['content']} for row in rows]


def session_exists(session_id):
    """检查会话是否存在"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT COUNT(*) AS cnt FROM chat_history WHERE session_id = %s",
        (session_id,)
    )
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result['cnt'] > 0


@bp.route('', methods=['POST'])
def chat():
    """
    POST /api/chat
    请求体: {"message": "...", "session_id": "...(可选)", "model": "deepseek(可选)"}
    """
    # 1. 取JSON数据
    data = request.get_json()
    if not data:
        return jsonify({'code': 400, 'message': '请求体必须是JSON'}), 400

    # 2. 校验 message
    message = data.get('message', '').strip()
    if not message:
        return jsonify({'code': 400, 'message': '缺少 message 参数'}), 400

    # 3. 处理 session_id（不传就新建）
    session_id = data.get('session_id')
    if not session_id:
        session_id = str(uuid.uuid4())

    # 4. 选择模型
    model = data.get('model', 'deepseek')
    if model not in AIClient.CONFIGS:
        return jsonify({'code': 400, 'message': f'不支持的模型: {model}，可选: deepseek, zhipu'}), 400

    # 5. 从数据库加载历史 + 创建客户端
    history = load_history(session_id)
    client = AIClient(model=model)
    client.load_history(history)

    # 6. 调用AI
    try:
        reply = client.ask(message)
    except Exception as e:
        return jsonify({'code': 500, 'message': f'AI服务调用失败: {str(e)}'}), 500

    # 7. 存消息到数据库（用户 + AI回复）
    save_message(session_id, 'user', message)
    save_message(session_id, 'assistant', reply)

    # 8. 返回响应
    return jsonify({
        'code': 200,
        'message': 'success',
        'data': {
            'reply': reply,
            'session_id': session_id,
        }
    })


@bp.route('/history', methods=['GET'])
def history():
    """
    GET /api/chat/history?session_id=xxx
    """
    # 1. 取参数
    session_id = request.args.get('session_id', '').strip()
    if not session_id:
        return jsonify({'code': 400, 'message': '缺少 session_id 参数'}), 400

    # 2. 检查会话是否存在
    if not session_exists(session_id):
        return jsonify({'code': 404, 'message': '会话不存在'}), 404

    # 3. 加载历史
    messages = load_history(session_id)

    # 4. 返回
    return jsonify({
        'code': 200,
        'message': 'success',
        'data': {
            'session_id': session_id,
            'messages': messages,
        }
    })
