from flask import Flask, redirect, url_for
from students import bp as students_bp
from courses import bp as courses_bp

app = Flask(__name__)
app.secret_key = 'dev-secret-key'

# 注册蓝图
app.register_blueprint(students_bp)
app.register_blueprint(courses_bp)


@app.route('/')
def index():
    return redirect(url_for('students.index'))


if __name__ == '__main__':
    app.run(debug=True)
