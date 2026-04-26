from flask import Blueprint, render_template, request, redirect, url_for, flash
from db import get_db

bp = Blueprint('courses', __name__, url_prefix='/courses')


# 查 — 课程列表
@bp.route('/')
def index():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM courses ORDER BY id DESC")
    courses = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('courses/index.html', courses=courses)


# 增 — 添加课程
@bp.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        name = request.form['name'].strip()
        teacher = request.form['teacher'].strip()
        hours = request.form['hours'].strip()

        errors = []
        if not name:
            errors.append('课程名不能为空')
        if not hours.isdigit() or int(hours) <= 0:
            errors.append('课时必须是正整数')

        if errors:
            for e in errors:
                flash(e, 'error')
            return render_template('courses/add.html', name=name, teacher=teacher, hours=hours)

        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO courses (name, teacher, hours) VALUES (%s, %s, %s)",
            (name, teacher, int(hours))
        )
        conn.commit()
        cursor.close()
        conn.close()

        flash(f'课程 {name} 添加成功！', 'success')
        return redirect(url_for('courses.index'))

    return render_template('courses/add.html')


# 删 — 删除课程
@bp.route('/delete/<int:id>')
def delete(id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM courses WHERE id = %s", (id,))
    conn.commit()
    affected = cursor.rowcount
    cursor.close()
    conn.close()

    if affected:
        flash('删除成功', 'success')
    else:
        flash('课程不存在', 'error')
    return redirect(url_for('courses.index'))
