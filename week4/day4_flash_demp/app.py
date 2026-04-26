import pymysql
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'dev-secret-key'

# 数据库连接配置
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '1234',
    'db': 'practice_db',
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor,
}


# 获取数据库连接
def get_db():
    return pymysql.connect(**DB_CONFIG)


# ============ 查（READ）：显示所有学生 ============
@app.route('/')
def index():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students ORDER BY id")
    students = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('students.html', students=students)


# ============ 增（CREATE）：添加学生 ============
@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        # 获取表单数据
        name = request.form['name'].strip()
        age = request.form['age'].strip()
        score = request.form['score'].strip()

        # 验证输入
        errors = []
        if not name:
            errors.append('姓名不能为空')
        if not age.isdigit() or int(age) < 0:
            errors.append('年龄必须是非负整数')
        try:
            score_val = float(score)
            if score_val < 0 or score_val > 100:
                errors.append('分数必须在0-100之间')
        except ValueError:
            errors.append('分数必须是数字')

        # 验证失败，回显已填内容
        if errors:
            for e in errors:
                flash(e, 'error')
            return render_template('add.html', name=name, age=age, score=score)

        # 验证通过，插入数据库
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO students (name, age, score) VALUES (%s, %s, %s)",
            (name, int(age), score_val)
        )
        conn.commit()
        cursor.close()
        conn.close()

        flash('添加成功！', 'success')
        return redirect(url_for('index'))

    # GET 请求：显示空的添加表单
    return render_template('add.html', name='', age='', score='')


# ============ 删（DELETE）：删除学生 ============
@app.route('/delete/<int:id>')
def delete(id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM students WHERE id = %s", (id,))
    conn.commit()
    affected = cursor.rowcount  # 获取受影响的行数
    cursor.close()
    conn.close()

    # 根据是否删除成功给出提示
    if affected:
        flash('删除成功！', 'success')
    else:
        flash('该学生不存在', 'error')
    return redirect(url_for('index'))


# ============ 改（UPDATE）：修改学生信息 ============
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    conn = get_db()
    cursor = conn.cursor()

    if request.method == 'POST':
        # 获取表单数据
        name = request.form['name'].strip()
        age = request.form['age'].strip()
        score = request.form['score'].strip()

        # 验证输入
        errors = []
        if not name:
            errors.append('姓名不能为空')
        if not age.isdigit() or int(age) < 0:
            errors.append('年龄必须是非负整数')
        try:
            score_val = float(score)
            if score_val < 0 or score_val > 100:
                errors.append('分数必须在0-100之间')
        except ValueError:
            errors.append('分数必须是数字')

        # 验证失败，回显已填内容
        if errors:
            for e in errors:
                flash(e, 'error')
            return render_template('edit.html',
                                   student={'id': id, 'name': name, 'age': age, 'score': score})

        # 验证通过，更新数据库
        cursor.execute(
            "UPDATE students SET name=%s, age=%s, score=%s WHERE id=%s",
            (name, int(age), score_val, id)
        )
        conn.commit()
        cursor.close()
        conn.close()

        flash('修改成功！', 'success')
        return redirect(url_for('index'))

    # GET 请求：查询原数据回填到表单
    cursor.execute("SELECT * FROM students WHERE id = %s", (id,))
    student = cursor.fetchone()
    cursor.close()
    conn.close()

    if not student:
        flash('该学生不存在', 'error')
        return redirect(url_for('index'))

    return render_template('edit.html', student=student)


if __name__ == '__main__':
    app.run(debug=True)
