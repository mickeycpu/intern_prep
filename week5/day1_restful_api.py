from flask import Flask, jsonify, request

app = Flask(__name__)

# ============ 模拟数据 ============
students = [
    {'id': 1, 'name': '张三', 'age': 20},
    {'id': 2, 'name': '李四', 'age': 22},
    {'id': 3, 'name': '王五', 'age': 19},
]

scores = [
    {'id': 1, 'student_name': '张三', 'subject': 'Python', 'score': 92},
    {'id': 2, 'student_name': '张三', 'subject': 'MySQL', 'score': 88},
    {'id': 3, 'student_name': '李四', 'subject': 'Python', 'score': 76},
]


# ============ 公共工具函数 ============
def paginate(data_list):
    """通用分页：从 request.args 取 page 和 per_page，返回分页后的数据"""
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))
    total = len(data_list)
    start = (page - 1) * per_page
    end = start + per_page
    return data_list[start:end], total, page, per_page


# =====================================================
#                     学生管理 API
# =====================================================

# 查全部学生（支持 ?name= 模糊搜索 + 分页）
@app.route('/api/students', methods=['GET'])
def get_students():
    result = students[:]
    # 搜索过滤
    name = request.args.get('name')
    if name:
        result = [s for s in result if name in s['name']]
    # 分页
    page_data, total, page, per_page = paginate(result)
    return jsonify({
        'code': 200,
        'data': page_data,
        'total': total,
        'page': page,
        'per_page': per_page
    })


# 查单个学生
@app.route('/api/students/<int:id>', methods=['GET'])
def get_student(id):
    for s in students:
        if s['id'] == id:
            return jsonify({'code': 200, 'data': s})
    return jsonify({'code': 404, 'message': '学生不存在'}), 404


# 新增学生
@app.route('/api/students', methods=['POST'])
def create_student():
    data = request.get_json()
    if not data or 'name' not in data or 'age' not in data:
        return jsonify({'code': 400, 'message': '缺少 name 或 age'}), 400
    new_student = {
        'id': students[-1]['id'] + 1 if students else 1,
        'name': data['name'],
        'age': data['age']
    }
    students.append(new_student)
    return jsonify({'code': 201, 'message': '创建成功', 'data': new_student}), 201


# 修改学生
@app.route('/api/students/<int:id>', methods=['PUT'])
def update_student(id):
    data = request.get_json()
    for s in students:
        if s['id'] == id:
            s['name'] = data.get('name', s['name'])
            s['age'] = data.get('age', s['age'])
            return jsonify({'code': 200, 'message': '修改成功', 'data': s})
    return jsonify({'code': 404, 'message': '学生不存在'}), 404


# 删除学生
@app.route('/api/students/<int:id>', methods=['DELETE'])
def delete_student(id):
    for i, s in enumerate(students):
        if s['id'] == id:
            students.pop(i)
            return jsonify({'code': 200, 'message': '删除成功'})
    return jsonify({'code': 404, 'message': '学生不存在'}), 404


# =====================================================
#                     成绩管理 API
# =====================================================

# 查全部成绩（支持 ?student_name= 筛选 + 分页）
@app.route('/api/scores', methods=['GET'])
def get_scores():
    result = scores[:]
    # 按学生名筛选
    student_name = request.args.get('student_name')
    if student_name:
        result = [sc for sc in result if sc['student_name'] == student_name]
    # 分页
    page_data, total, page, per_page = paginate(result)
    return jsonify({
        'code': 200,
        'data': page_data,
        'total': total,
        'page': page,
        'per_page': per_page
    })


# 查单条成绩
@app.route('/api/scores/<int:id>', methods=['GET'])
def get_score(id):
    for sc in scores:
        if sc['id'] == id:
            return jsonify({'code': 200, 'data': sc})
    return jsonify({'code': 404, 'message': '成绩不存在'}), 404


# 新增成绩（验证 score 0-100）
@app.route('/api/scores', methods=['POST'])
def create_score():
    data = request.get_json()
    if not data or 'student_name' not in data or 'subject' not in data or 'score' not in data:
        return jsonify({'code': 400, 'message': '缺少 student_name、subject 或 score'}), 400
    if not isinstance(data['score'], (int, float)) or data['score'] < 0 or data['score'] > 100:
        return jsonify({'code': 400, 'message': '分数必须在 0-100 之间'}), 400
    new_score = {
        'id': scores[-1]['id'] + 1 if scores else 1,
        'student_name': data['student_name'],
        'subject': data['subject'],
        'score': data['score']
    }
    scores.append(new_score)
    return jsonify({'code': 201, 'message': '创建成功', 'data': new_score}), 201


# 修改成绩
@app.route('/api/scores/<int:id>', methods=['PUT'])
def update_score(id):
    data = request.get_json()
    # 如果传了 score 字段，验证范围
    if 'score' in data:
        if not isinstance(data['score'], (int, float)) or data['score'] < 0 or data['score'] > 100:
            return jsonify({'code': 400, 'message': '分数必须在 0-100 之间'}), 400
    for sc in scores:
        if sc['id'] == id:
            sc['student_name'] = data.get('student_name', sc['student_name'])
            sc['subject'] = data.get('subject', sc['subject'])
            sc['score'] = data.get('score', sc['score'])
            return jsonify({'code': 200, 'message': '修改成功', 'data': sc})
    return jsonify({'code': 404, 'message': '成绩不存在'}), 404


# 删除成绩
@app.route('/api/scores/<int:id>', methods=['DELETE'])
def delete_score(id):
    for i, sc in enumerate(scores):
        if sc['id'] == id:
            scores.pop(i)
            return jsonify({'code': 200, 'message': '删除成功'})
    return jsonify({'code': 404, 'message': '成绩不存在'}), 404


if __name__ == '__main__':
    app.run(debug=True)
