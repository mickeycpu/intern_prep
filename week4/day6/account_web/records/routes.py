"""记账蓝图 — 增删改查路由"""
from flask import Blueprint, render_template, request, redirect, url_for, flash
from db import get_db

bp = Blueprint('records', __name__, url_prefix='/records')


@bp.route('/')
def index():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM records ORDER BY created_at DESC")
    records = cursor.fetchall()
    cursor.execute("""
        SELECT
            COALESCE(SUM(CASE WHEN type='income' THEN amount ELSE 0 END), 0) AS total_income,
            COALESCE(SUM(CASE WHEN type='expense' THEN amount ELSE 0 END), 0) AS total_expense
        FROM records
    """)
    stats = cursor.fetchone()
    cursor.close()
    conn.close()
    balance = stats['total_income'] - stats['total_expense']
    return render_template('records/index.html',
                           records=records, stats=stats, balance=balance)


@bp.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        type_ = request.form['type']
        category = request.form['category'].strip()
        amount = request.form['amount'].strip()
        note = request.form.get('note', '').strip()

        errors = []
        if not category:
            errors.append('分类不能为空')
        if not amount:
            errors.append('金额不能为空')
        else:
            try:
                amount = float(amount)
                if amount <= 0:
                    errors.append('金额必须大于0')
            except ValueError:
                errors.append('金额格式不正确')

        if errors:
            for e in errors:
                flash(e, 'error')
            return render_template('records/add.html',
                                   type_=type_, category=category,
                                   amount=request.form['amount'], note=note)

        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO records (type, category, amount, note) VALUES (%s, %s, %s, %s)",
            (type_, category, amount, note)
        )
        conn.commit()
        cursor.close()
        conn.close()
        flash('添加成功！', 'success')
        return redirect(url_for('records.index'))

    return render_template('records/add.html')


@bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    conn = get_db()
    cursor = conn.cursor()

    if request.method == 'POST':
        type_ = request.form['type']
        category = request.form['category'].strip()
        amount = request.form['amount'].strip()
        note = request.form.get('note', '').strip()

        errors = []
        if not category:
            errors.append('分类不能为空')
        if not amount:
            errors.append('金额不能为空')
        else:
            try:
                amount = float(amount)
                if amount <= 0:
                    errors.append('金额必须大于0')
            except ValueError:
                errors.append('金额格式不正确')

        if errors:
            for e in errors:
                flash(e, 'error')
            cursor.close()
            conn.close()
            return render_template('records/edit.html',
                                   record={'id': id, 'type': type_,
                                           'category': category,
                                           'amount': request.form['amount'],
                                           'note': note})

        cursor.execute(
            "UPDATE records SET type=%s, category=%s, amount=%s, note=%s WHERE id=%s",
            (type_, category, amount, note, id)
        )
        conn.commit()
        cursor.close()
        conn.close()
        flash('修改成功！', 'success')
        return redirect(url_for('records.index'))

    cursor.execute("SELECT * FROM records WHERE id = %s", (id,))
    record = cursor.fetchone()
    cursor.close()
    conn.close()

    if not record:
        flash('记录不存在', 'error')
        return redirect(url_for('records.index'))

    return render_template('records/edit.html', record=record)


@bp.route('/delete/<int:id>')
def delete(id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM records WHERE id = %s", (id,))
    conn.commit()
    cursor.close()
    conn.close()
    flash('删除成功！', 'success')
    return redirect(url_for('records.index'))
