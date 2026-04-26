"""主入口 — 注册蓝图、启动Flask"""
from flask import Flask
from records import bp as records_bp

app = Flask(__name__)
app.secret_key = 'account_web_secret_key'

app.register_blueprint(records_bp)


@app.route('/')
def index():
    from flask import redirect, url_for
    return redirect(url_for('records.index'))


if __name__ == '__main__':
    app.run(debug=True)
