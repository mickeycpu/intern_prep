# Week 4 学习总结 — Flask框架入门

> 🗓️ 12周学习计划 第4周 | 每天2.5小时 | 主题：Flask Web开发全链路

---

## 📌 本周概览

| 天 | 主题 | 核心产出 |
|---|------|---------|
| Day1 | Flask安装 / 路由 / 路由变量 | hello_flask.py |
| Day2 | 模板渲染 Jinja2 | 5个模板练习项目 |
| Day3 | 表单处理 GET/POST | 注册表单（3轮迭代） |
| Day4 | Flask连接MySQL | 学生管理系统增删改查 |
| Day5 | 蓝图 Blueprint / 项目结构 | 学生+课程双蓝图模块化项目 |
| Day6 | 综合项目：记账Web版 | Flask+MySQL+Jinja2 完整Web应用 |

---

## 🧱 Day 1 — Flask基础 / 路由 / 路由变量

### Flask 运行机制

```python
from flask import Flask
app = Flask(__name__)

@app.route('/')
def index():
    return '这是首页'

if __name__ == '__main__':
    app.run(debug=True)
```

- `app = Flask(__name__)` — 创建应用实例，`__name__` 用于定位资源文件
- `debug=True` — 开发时自动重启 + 浏览器显示完整错误堆栈（上线必须关闭）

### 路由与路由变量

```python
@app.route('/user/<name>')          # 字符串类型（默认）
def show_user(name):
    return f'你好，{name}！'

@app.route('/score/<int:num>')      # 整型，自动转换
def show_score(num):
    return f'分数：{num}'
```

- 支持类型：`string`（默认）/ `int` / `float` / `path`
- 路由变量名必须和函数参数名一致，否则 **500 错误**（不是404）
- 两个相同路由会**静默覆盖**，不报错

---

## 🎨 Day 2 — 模板渲染 Jinja2

### 三种核心语法

| 语法 | 作用 | 是否输出到HTML |
|------|------|:---:|
| `{{ 变量名 }}` | 输出变量值 | ✅ |
| `{% 逻辑 %}` | 控制逻辑（if/for） | ❌ |
| `{# 注释 #}` | 模板注释 | ❌ |

### 模板继承（面试高频）

```html
<!-- 父模板 base.html -->
<nav>导航栏（共享）</nav>
{% block content %}{% endblock %}
<footer>页脚（共享）</footer>

<!-- 子模板 index.html -->
{% extends "base.html" %}
{% block content %}
<h1>首页内容</h1>
{% endblock %}
```

子模板只写 `{% block %}` 里的内容，导航栏、页脚等共享部分自动继承。

### 过滤器与循环变量

```html
{{ name | upper }}                          <!-- 转大写 -->
{{ nickname | default('匿名') }}             <!-- 空值默认 -->
{{ "%.2f"|format(amount) }}                 <!-- 金额格式化 -->

{% for item in items %}
    {{ loop.index }}. {{ item }}            <!-- 从1开始 -->
    {% if loop.first %}⭐{% endif %}
{% endfor %}
```

**踩坑记录：** `loop.index` 从 **1** 开始（不是0）；模板变量名拼错→静默显示空白，不报错。

---

## 📝 Day 3 — 表单处理 GET/POST

### GET vs POST

| | GET | POST |
|---|-----|------|
| 数据位置 | URL 里（`/search?keyword=xxx`） | 请求体里 |
| 适用场景 | 查询、浏览 | 提交、注册、修改 |
| 安全性 | 参数可见 | 参数不可见 |

### request.form vs request.args

```python
request.form['username']   # ← 取 POST 表单数据
request.args['keyword']    # ← 取 GET URL 参数
```

### POST/Redirect/GET 模式（防重复提交）

```python
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # 处理表单...
        flash('注册成功！', 'success')
        return redirect(url_for('index'))    # ✅ redirect，不是 render_template
    return render_template('register.html')   # GET 显示表单
```

**为什么用 redirect？** 浏览器地址栏还停在 `/register`，用户刷新会重复 POST。redirect 后地址变成 `/`，刷新只 GET 首页。

### flash 闪现消息

```python
flash('注册成功！', 'success')       # 存入 session

# 模板端（写在 base.html 里，全局继承）
{% with messages = get_flashed_messages(with_categories=true) %}
    {% for category, msg in messages %}
        <div class="flash {{ category }}">{{ msg }}</div>
    {% endfor %}
{% endwith %}
```

flash 消息取一次就消失，刷新页面就没了。

---

## 🗄️ Day 4 — Flask连接MySQL

### 数据库配置集中管理

```python
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', ''),
    'db': 'flask_demo',
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor,  # 全局字典返回
}

def get_db():
    return pymysql.connect(**DB_CONFIG)
```

- `DictCursor` 配置一次全局生效，查询结果直接返回字典
- 密码从 `.env` 读取，**绝不上 GitHub**

### CRUD 四件套完整流程

```
查（READ）     SELECT *        → GET  /         → render_template 展示列表
增（CREATE）   INSERT INTO     → GET+POST /add  → 表单→验证→insert→redirect
改（UPDATE）   UPDATE SET      → GET+POST /edit → 回填→修改→redirect
删（DELETE）   DELETE WHERE id → GET  /delete/<id> → redirect 回列表
```

每个路由同一套模式：**连库 → 执行SQL → 关连接 → 渲染模板或重定向**

### 参数化查询防注入

```python
# ✅ 安全 — 参数当数据处理
cursor.execute("DELETE FROM records WHERE id = %s", (id,))

# ❌ 危险 — 用户输入直接拼入SQL
cursor.execute(f"DELETE FROM records WHERE id = '{id}'")
```

### 事务 + 行锁

```python
try:
    conn.begin()
    cursor.execute("SELECT balance FROM accounts WHERE name=%s FOR UPDATE", (name,))  # 行锁
    cursor.execute("UPDATE accounts SET balance=balance-%s WHERE name=%s", (amount, name))
    conn.commit()
except:
    conn.rollback()
```

---

## 🧩 Day 5 — 蓝图 Blueprint / 项目结构

### 蓝图是什么

蓝图 = 路由的分组容器，把不同功能的路由拆到不同文件里。

```
公司 → Flask应用    部门 → 蓝图    员工 → 路由函数
```

### 创建与注册蓝图

```python
# students/routes.py
bp = Blueprint('students', __name__, url_prefix='/students')

@bp.route('/')              # 实际访问 /students/
def index():
    return render_template('students/index.html')

# app.py
from students import bp as students_bp
app.register_blueprint(students_bp)   # 不注册 → 404
```

- `url_prefix` 自动给蓝图内所有路由加前缀
- `url_for('students.index')` — 蓝图路由的 url_for 写法（蓝图名.函数名）

### 标准项目结构

```
flask_project/
├── app.py              # 主入口（注册蓝图、启动）
├── db.py               # 公共数据库模块（get_db）
├── init_db.py          # 建表脚本
├── templates/
│   ├── base.html       # 全局父模板
│   ├── students/       # 学生模板
│   └── courses/        # 课程模板
├── students/           # 学生蓝图
│   ├── __init__.py
│   └── routes.py
└── courses/            # 课程蓝图
    ├── __init__.py
    └── routes.py
```

**核心原则：** 谁都要用的东西（如 `get_db()`）放公共模块 `db.py`，不放任何一方，避免依赖混乱。

---

## 🚀 Day 6 — 综合项目：记账Web版

### 项目架构

```
account_web/
├── app.py                    # 主入口 + 蓝图注册 + secret_key
├── db.py                     # DB_CONFIG + get_db()
├── init_db.py                # 建表脚本（运行一次）
├── records/                  # 记账蓝图
│   ├── __init__.py
│   └── routes.py             # CRUD 四个路由
└── templates/
    ├── base.html             # 父模板（导航 + flash消息）
    └── records/
        ├── index.html        # 记录列表（循环+过滤器+条件判断）
        └── add.html          # 添加表单（回填+验证）
```

### 核心代码模式

```python
# records/routes.py — 添加记录
@bp.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        conn = get_db()
        cursor = conn.cursor()
        try:
            type_ = request.form['type']
            category = request.form['category'].strip()
            amount = Decimal(request.form['amount'].strip())

            # 验证
            errors = []
            if not category:
                errors.append('分类不能为空')
            if amount <= 0:
                errors.append('金额必须大于0')

            if errors:
                for e in errors:
                    flash(e, 'error')
                return render_template('records/add.html',
                                       type_=type_, category=category,
                                       amount=request.form['amount'])

            # 插入数据库
            cursor.execute(
                "INSERT INTO records (type, category, amount) VALUES (%s, %s, %s)",
                (type_, category, amount)
            )
            conn.commit()
            flash('添加成功！', 'success')
            return redirect(url_for('records.index'))  # 防重复提交
        finally:
            cursor.close()
            conn.close()

    return render_template('records/add.html')
```

### 关键细节

| 要点 | 说明 |
|------|------|
| `%s` 参数化查询 | 防 SQL 注入，不能用 f-string 拼接 |
| redirect 不用 render_template | 防刷新重复提交（POST/Redirect/GET） |
| 验证失败用 render_template | 保留用户已填的值，不跳转 |
| 所有分支都要 close 连接 | 包括验证失败路径，否则连接泄漏 |
| `value="{{ category or '' }}"` | 表单回填，验证失败时保留输入 |
| `confirm('确定删除吗？')` | 删除前弹窗确认 |
| `"%.2f"\|format(amount)` | 过滤器格式化金额 |
| `app.secret_key` | flash 消息必须有，否则报错 |

---

## 📊 本周技能收获

### 新掌握技能清单

- **Flask 框架核心**：路由、路由变量、debug模式、`if __name__ == '__main__'`
- **Jinja2 模板引擎**：三种语法、模板继承、过滤器、循环变量、条件判断
- **表单处理**：GET/POST、request.form/request.args、redirect防重复提交、flash闪现消息、表单验证与回填
- **数据库集成**：Flask+MySQL全链路、DB_CONFIG集中管理、DictCursor全局配置、参数化查询防注入、事务+行锁
- **项目架构**：蓝图Blueprint、url_prefix前缀、`__init__.py`变Python包、公共模块提取、模块化项目结构
- **综合实践**：完整CRUD Web应用、POST/Redirect/GET模式、连接管理、模板继承实战

### 产出项目

| 项目 | 技术栈 | 说明 |
|------|--------|------|
| hello_flask.py | Flask | 路由、路由变量、动态路由 |
| flask_demo/ | Flask + Jinja2 | 5个模板渲染练习 |
| day3_round1~3_register.py | Flask + 表单 | 注册表单3轮迭代 |
| day4_flash_demo/ | Flask + MySQL | 学生管理系统增删改查 |
| day5_blueprint_demo/ | Flask + Blueprint | 学生+课程双蓝图模块化 |
| **day6_account_web/** | **Flask + MySQL + Jinja2** | **记账Web版 — 完整CRUD应用** |

---

## 🔗 技术栈关联图

```
用户请求
   ↓
Flask 路由（@app.route / @bp.route）
   ↓
业务逻辑（参数化查询 / 事务 / 验证）
   ↓
pymysql（DictCursor / get_db()）
   ↓
MySQL（CRUD / 行锁 / 索引）
   ↓
Jinja2 模板（继承 / 过滤器 / 循环）
   ↓
HTML 响应（render_template / redirect）
```
