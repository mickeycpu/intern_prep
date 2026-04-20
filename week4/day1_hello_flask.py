from flask import Flask

# 创建 Flask 应用实例，__name__ 用于定位资源文件
app = Flask(__name__)


# 首页路由：访问 http://127.0.0.1:5000/
@app.route('/')
def index():
    return '欢迎来到我的Flask应用！'


# 关于页面：访问 http://127.0.0.1:5000/about
@app.route('/about')
def about():
    return '我是张添宇，正在学习Flask'


# 动态路由：URL 中的 <name> 会作为参数传给函数
# 例如访问 /user/张三 → name = '张三'
@app.route('/user/<name>')
def show_user(name):
    return f'你好，{name}！'


# 带类型的动态路由：<int:num> 限定只能传整数
# 访问 /score/95 → num = 95（整数）
# 访问 /score/abc → 404，因为 abc 不是整数
@app.route('/score/<int:num>')
def show_score(num):
    return f'你的分数是：{num}'


# 只在直接运行此文件时启动服务器，被 import 时不启动
if __name__ == '__main__':
    # debug=True：改代码自动重启 + 浏览器显示错误详情（上线必须关）
    app.run(debug=True)
