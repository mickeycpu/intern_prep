from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'dev_key_123'

users = []


@app.route('/')
def index():
    return f'<h1>已注册用户：{len(users)} 人</h1><a href="/register">去注册</a>'


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username'].strip()  # 去首尾空格
        password = request.form['password']
        email = request.form['email'].strip()

        # ===== 验证逻辑 =====
        errors = []

        if not username:
            errors.append('用户名不能为空')
        if not email:
            errors.append('邮箱不能为空')
        if not password:
            errors.append('密码不能为空')
        elif len(password) < 6:
            errors.append('密码长度不能少于6位')

        # 有错误 → 不跳转，回到表单并显示错误
        if errors:
            for err in errors:
                flash(err, 'error')
            # 把用户已填的值传回去，不用重新填
            return render_template('register2.html',
                                   username=username, email=email)

        # 验证通过
        users.append({'username': username, 'email': email})
        flash(f'注册成功！欢迎 {username}', 'success')
        return redirect(url_for('index'))

    return render_template('register2.html')


if __name__ == '__main__':
    app.run(debug=False, port=5050)

