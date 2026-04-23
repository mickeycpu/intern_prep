from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'dev_key_123'

users = []


@app.route('/')
def index():
    return render_template('index3.html', users=users)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password']
        email = request.form['email'].strip()

        errors = []
        if not username:
            errors.append('用户名不能为空')
        if not email:
            errors.append('邮箱不能为空')
        if not password:
            errors.append('密码不能为空')
        elif len(password) < 6:
            errors.append('密码长度不能少于6位')

        if errors:
            for err in errors:
                flash(err, 'error')
            return render_template('register3.html',
                                   username=username, email=email)

        users.append({'username': username, 'email': email})
        flash('注册成功！', 'success')

        # 跳转到结果页，用路由变量传用户名
        return redirect(url_for('result', username=username))

    return render_template('register3.html')


@app.route('/result/<username>')
def result():
    # 从 users 列表中找到这个用户
    user = None
    for u in users:
        if u['username'] == username:
            user = u
            break

    if user is None:
        flash('用户不存在', 'error')
        return redirect(url_for('index'))

    return render_template('result.html', user=user)


if __name__ == '__main__':
    app.run(debug=True, port=5050)

