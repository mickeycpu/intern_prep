from flask import Blueprint, render_template, request, redirect, url_for, flash
from db import get_db

bp = Blueprint('students', __name__, url_prefix='/students')


# 查 — 学生列表（含搜索）
@bp.route('/')
def index():
    keyword = request.args.get('keyword', '').strip()
    conn = get_db()
    cursor = conn.cursor()

    if keyword:
        cursor.execute(
            "SELECT * FROM students WHERE name LIKE %s ORDER BY id DESC",
            (f"%{keyword}%",)
        )
    else:
        cursor.execute("SELECT * FROM students ORDER BY id DESC")

    students = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('students/index.html', students=students, keyword=keyword)


# 增 — 添加学生
@bp.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        name = request.form['name'].strip()
        age = request.form['age'].strip()
        score = request.form['score'].strip()

        errors = []
        if not name:
            errors.append('姓名不能为空')
        if not age.isdigit() or int(age) < 0:
            errors.append('年龄必须是非负整数')
        try:
            score_val = float(score)
            if score_val < 0 or score_val > 100:
                errors.append('成绩必须在0-100之间')
        except ValueError:
            errors.append('成绩必须是数字')

        if errors:
            for e in errors:
                flash(e, 'error')
            return render_template('students/add.html', name=name, age=age, score=score)

        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO students (name, age, score) VALUES (%s, %s, %s)",
            (name, int(age), score_val)
        )
        conn.commit()
        cursor.close()
        conn.close()

        flash(f'学生 {name} 添加成功！', 'success')
        return redirect(url_for('students.index'))

    return render_template('students/add.html')


# 改 — 编辑学生
@bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    conn = get_db()
    cursor = conn.cursor()

    if request.method == 'POST':
        name = request.form['name'].strip()
        age = request.form['age'].strip()
        score = request.form['score'].strip()

        errors = []
        if not name:
            errors.append('姓名不能为空')

        if errors:
            for e in errors:
                flash(e, 'error')
            return render_template('students/edit.html',
                                   student={'id': id, 'name': name, 'age': age, 'score': score})

        cursor.execute(
            "UPDATE students SET name=%s, age=%s, score=%s WHERE id=%s",
            (name, int(age), float(score), id)
        )
        conn.commit()
        cursor.close()
        conn.close()

        flash(f'学生 {name} 修改成功！', 'success')
        return redirect(url_for('students.index'))

    cursor.execute("SELECT * FROM students WHERE id = %s", (id,))
    student = cursor.fetchone()
    cursor.close()
    conn.close()

    if not student:
        flash('学生不存在', 'error')
        return redirect(url_for('students.index'))

    return render_template('students/edit.html', student=student)


# 删 — 删除学生
@bp.route('/delete/<int:id>')
def delete(id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM students WHERE id = %s", (id,))
    conn.commit()
    affected = cursor.rowcount
    cursor.close()
    conn.close()

    if affected:
        flash('删除成功', 'success')
    else:
        flash('学生不存在', 'error')
    return redirect(url_for('students.index'))
