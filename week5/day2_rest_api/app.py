from flask import Flask, jsonify, request
from db import get_db

app = Flask(__name__)


# ============ 公共分页函数 ============
def paginate(data_list):
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))
    total = len(data_list)
    start = (page - 1) * per_page
    end = start + per_page
    return data_list[start:end], total, page, per_page


# =====================================================
# 学生管理 API
# =====================================================

@app.route('/api/students', methods=['GET'])
def get_students():
    conn = get_db()
    cursor = conn.cursor()
    sql = "SELECT * FROM students"
    params = []
    name = request.args.get('name')
    if name:
        sql += " WHERE name LIKE %s"
        params.append(f"%{name}%")
    sql += " ORDER BY id ASC"
    cursor.execute(sql, params)
    all_data = cursor.fetchall()
    page_data, total, page, per_page = paginate(all_data)
    cursor.close()
    conn.close()
    return jsonify({'code': 200, 'data': page_data, 'total': total, 'page': page, 'per_page': per_page})


@app.route('/api/students/<int:id>', methods=['GET'])
def get_student(id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students WHERE id = %s", (id,))
    student = cursor.fetchone()
    cursor.close()
    conn.close()
    if student:
        return jsonify({'code': 200, 'data': student})
    return jsonify({'code': 404, 'message': '学生不存在'}), 404


@app.route('/api/students', methods=['POST'])
def create_student():
    data = request.get_json()
    if not data or 'name' not in data or 'age' not in data:
        return jsonify({'code': 400, 'message': '缺少 name 或 age'}), 400
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO students (name, age) VALUES (%s, %s)", (data['name'], data['age']))
    conn.commit()
    new_id = cursor.lastrowid
    cursor.close()
    conn.close()
    return jsonify({'code': 201, 'message': '创建成功', 'data': {'id': new_id, 'name': data['name'], 'age': data['age']}}), 201


@app.route('/api/students/<int:id>', methods=['PUT'])
def update_student(id):
    data = request.get_json()
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE students SET name=%s, age=%s WHERE id=%s", (data.get('name'), data.get('age'), id))
    conn.commit()
    affected = cursor.rowcount
    cursor.close()
    conn.close()
    if affected:
        return jsonify({'code': 200, 'message': '修改成功'})
    return jsonify({'code': 404, 'message': '学生不存在'}), 404


@app.route('/api/students/<int:id>', methods=['DELETE'])
def delete_student(id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM students WHERE id = %s", (id,))
    conn.commit()
    affected = cursor.rowcount
    cursor.close()
    conn.close()
    if affected:
        return jsonify({'code': 200, 'message': '删除成功'})
    return jsonify({'code': 404, 'message': '学生不存在'}), 404


# =====================================================
# 成绩管理 API
# =====================================================

@app.route('/api/scores', methods=['GET'])
def get_scores():
    conn = get_db()
    cursor = conn.cursor()
    sql = "SELECT * FROM scores"
    params = []
    student_name = request.args.get('student_name')
    if student_name:
        sql += " WHERE student_name = %s"
        params.append(student_name)
    sql += " ORDER BY id ASC"
    cursor.execute(sql, params)
    all_data = cursor.fetchall()
    page_data, total, page, per_page = paginate(all_data)
    cursor.close()
    conn.close()
    return jsonify({'code': 200, 'data': page_data, 'total': total, 'page': page, 'per_page': per_page})


@app.route('/api/scores/<int:id>', methods=['GET'])
def get_score(id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM scores WHERE id = %s", (id,))
    score = cursor.fetchone()
    cursor.close()
    conn.close()
    if score:
        return jsonify({'code': 200, 'data': score})
    return jsonify({'code': 404, 'message': '成绩不存在'}), 404


@app.route('/api/scores', methods=['POST'])
def create_score():
    data = request.get_json()
    if not data or 'student_name' not in data or 'subject' not in data or 'score' not in data:
        return jsonify({'code': 400, 'message': '缺少 student_name、subject 或 score'}), 400
    if not isinstance(data['score'], (int, float)) or data['score'] < 0 or data['score'] > 100:
        return jsonify({'code': 400, 'message': '分数必须在 0-100 之间'}), 400
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO scores (student_name, subject, score) VALUES (%s, %s, %s)",
                   (data['student_name'], data['subject'], data['score']))
    conn.commit()
    new_id = cursor.lastrowid
    cursor.close()
    conn.close()
    return jsonify({'code': 201, 'message': '创建成功', 'data': {'id': new_id, 'student_name': data['student_name'], 'subject': data['subject'], 'score': data['score']}}), 201


@app.route('/api/scores/<int:id>', methods=['PUT'])
def update_score(id):
    data = request.get_json()
    if 'score' in data:
        if not isinstance(data['score'], (int, float)) or data['score'] < 0 or data['score'] > 100:
            return jsonify({'code': 400, 'message': '分数必须在 0-100 之间'}), 400
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE scores SET student_name=%s, subject=%s, score=%s WHERE id=%s",
                   (data.get('student_name'), data.get('subject'), data.get('score'), id))
    conn.commit()
    affected = cursor.rowcount
    cursor.close()
    conn.close()
    if affected:
        return jsonify({'code': 200, 'message': '修改成功'})
    return jsonify({'code': 404, 'message': '成绩不存在'}), 404


@app.route('/api/scores/<int:id>', methods=['DELETE'])
def delete_score(id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM scores WHERE id = %s", (id,))
    conn.commit()
    affected = cursor.rowcount
    cursor.close()
    conn.close()
    if affected:
        return jsonify({'code': 200, 'message': '删除成功'})
    return jsonify({'code': 404, 'message': '成绩不存在'}), 404


# =====================================================
# 挑战：查某个学生的所有成绩
# =====================================================

@app.route('/api/students/<name>/scores', methods=['GET'])
def get_student_scores(name):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT subject, score FROM scores WHERE student_name = %s", (name,))
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify({'code': 200, 'student': name, 'data': data})


if __name__ == '__main__':
    app.run(debug=True)
