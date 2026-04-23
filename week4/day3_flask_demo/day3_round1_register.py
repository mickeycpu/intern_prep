from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'dev_key_123'  # flash 需要 secret_key

# 模拟数据库，存注册用户
users = []


@app.route('/')
def index():
    return f'<h1>已注册用户：{len(users)} 人</h1><a href="/register">去注册</a>'


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # 从表单取数据
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

        # 存入列表（实际项目存数据库）
        users.append({'username': username, 'email': email})
        flash('注册成功！', 'success')

        # 跳转到首页，避免刷新重复提交
        return redirect(url_for('index'))

    # GET 请求：显示注册表单
    return render_template('register.html')


if __name__ == '__main__':
    app.run(debug=False, port=5050)

