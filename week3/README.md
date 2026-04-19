# Week 3 — MySQL 进阶与 Python 数据库操作

> 📅 学习周期：12周 Python 后端 + AI 应用开发计划 · 第三周
> 🎯 本阶段目标：掌握 MySQL 高级查询、性能优化，并用 Python (pymysql) 实现完整的数据库 CRUD 与项目持久化

---

## 📖 知识体系总览

```
MySQL 进阶
├── 多表查询：JOIN（INNER / LEFT）与子查询
├── 性能优化：索引原理、EXPLAIN 分析
└── 数据安全：事务（ACID）、并发控制

Python 操作数据库
├── pymysql 基础：连接 → 游标 → 执行 → 提交 → 关闭
├── 安全实践：参数化查询防 SQL 注入、.env 管理密码
├── OOP 封装：数据库操作类 + 上下文管理器（with）
└── 综合项目：MySQL 版 CLI 记账本
```

---

## 1️⃣ JOIN 与子查询

### 核心概念

多表查询是关系型数据库的灵魂。现实中的数据不会全塞在一张表里——学生表、成绩表、课程表各管各的，靠外键关联。

| 类型 | 行为 | 使用场景 |
|------|------|---------|
| `INNER JOIN` | 只返回两表都能匹配的行 | 只关心有对应关系的数据 |
| `LEFT JOIN` | 左表全部返回，右表没匹配填 NULL | 需要保留左表全部记录 |

### 代码示例

```sql
-- 查询每个学生的选课情况（没选课的学生也显示）
SELECT s.name, c.course_name, sc.score
FROM students s
LEFT JOIN score sc ON s.id = sc.student_id
LEFT JOIN courses c ON sc.course_id = c.id;

-- 子查询：查成绩高于平均分的学生
SELECT name, score FROM students
WHERE score > (SELECT AVG(score) FROM students);
```

### 要点
- `ON` 指定连接条件，`WHERE` 过滤结果——别搞混
- 子查询可以嵌套，但层级越深越难维护，能用 JOIN 就不用子查询

---

## 2️⃣ 索引与性能优化

### 为什么需要索引

没有索引的查询 = 翻书没有目录，逐页找。数据量一大（万级以上），性能断崖式下降。

### 索引原理（B+ 树）

MySQL 默认用 B+ 树索引，数据按排序结构组织，查询从树根到叶子只需 **O(log n)** 次比较，远优于全表扫描的 **O(n)**。

### EXPLAIN 分析

```sql
EXPLAIN SELECT * FROM orders WHERE user_id = 100;
```

关注 `type` 字段：
- `ALL` → 全表扫描 ❌（需要优化）
- `ref` / `range` → 走了索引 ✅
- `const` → 主键精确匹配，最快 ✅

### 索引使用原则

| ✅ 该加索引 | ❌ 不该加 |
|------------|----------|
| WHERE 频繁查询的字段 | 经常增删的表（索引维护有开销） |
| JOIN 的关联字段 | 区分度低的字段（如性别） |
| ORDER BY / GROUP BY 字段 | 数据量很小的表 |

### 要点
- 索引是**空间换时间**，加速读、拖慢写
- 复合索引遵循**最左前缀匹配**原则
- `SELECT *` 可能导致索引失效，尽量只查需要的列

---

## 3️⃣ 事务与 ACID

### 什么是事务

把多条 SQL 打包成一个整体：**要么全成功，要么全失败**。经典场景——转账：A 扣钱和 B 加钱必须同时成立。

```sql
BEGIN;
  UPDATE accounts SET balance = balance - 500 WHERE name = 'Alice';
  UPDATE accounts SET balance = balance + 500 WHERE name = 'Bob';
COMMIT;  -- 全部成功，生效
-- 如果中间出错：
ROLLBACK;  -- 全部撤销，回到初始状态
```

### ACID 四大特性

| 特性 | 含义 | 一句话理解 |
|------|------|-----------|
| **A**tomicity 原子性 | 要么全做，要么全不做 | 转账不能只扣不加 |
| **C**onsistency 一致性 | 数据从一个合法状态到另一个合法状态 | 总金额不能凭空变化 |
| **I**solation 隔离性 | 多个事务互不干扰 | 两人同时转账不出错 |
| **D**urability 持久性 | COMMIT 后数据永久保存 | 断电也不丢（redo log） |

### 并发问题：竞态条件

两个事务同时读余额 → 都判断"够" → 各扣一笔 → 透支了。

解决：把检查和操作放在**同一事务**内，用 `SELECT ... FOR UPDATE` 加行锁，让第二个事务等第一个完成。

---

## 4️⃣ pymysql 实战

### 五步操作流程

```python
import pymysql

conn = pymysql.connect(host='localhost', user='root', password='xxx', db='test')  # ① 连接
cursor = conn.cursor(pymysql.cursors.DictCursor)   # ② 游标（DictCursor 返回字典）

try:
    cursor.execute("SELECT * FROM students WHERE age > %s", (18,))  # ③ 执行（参数化）
    rows = cursor.fetchall()                                         #    取结果
    conn.commit()  # ④ 提交
except Exception as e:
    conn.rollback()  # ④ 回滚
finally:
    cursor.close()   # ⑤ 关闭（先游标后连接）
    conn.close()
```

### 关键方法速查

| 方法 | 返回值 | 用途 |
|------|--------|------|
| `execute(sql, params)` | 影响行数 | 执行单条 SQL |
| `executemany(sql, data)` | — | 批量插入（减少网络往返） |
| `fetchone()` | 元组/字典 或 `None` | 取一行 |
| `fetchall()` | 列表 | 取全部（大表慎用） |
| `rowcount` | int | 上次操作影响的行数 |

### 安全实践

```python
# ✅ 参数化查询 — 防 SQL 注入
cursor.execute("SELECT * FROM users WHERE name = %s", (name,))

# ❌ f-string 拼接 — 注入漏洞
cursor.execute(f"SELECT * FROM users WHERE name = '{name}'")
# 用户输入 ' OR '1'='1 即可查出所有数据

# ✅ .env 管理密码 — 绝不上 GitHub
from dotenv import load_dotenv
import os
load_dotenv()
DB_PASSWORD = os.getenv('DB_PASSWORD')
```

---

## 5️⃣ OOP 封装数据库操作

### 设计思路

把连接、CRUD、资源清理全部封装进类，对外只暴露简洁方法：

```python
class StudentDB:
    def __init__(self):
        self.conn = pymysql.connect(**DB_CONFIG)
        self.cursor = self.conn.cursor(pymysql.cursors.DictCursor)
        self._init_table()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def insert(self, name, age, score):
        self.cursor.execute(
            "INSERT INTO students (name, age, score) VALUES (%s, %s, %s)",
            (name, age, score)
        )
        self.conn.commit()
        return self.cursor.lastrowid

    def search(self, keyword):
        self.cursor.execute(
            "SELECT * FROM students WHERE name LIKE %s",
            (f"%{keyword}%",)
        )
        return self.cursor.fetchall()

    def close(self):
        self.cursor.close()
        self.conn.close()

# 使用：with 语法自动管理资源
with StudentDB() as db:
    db.insert("张三", 22, 85.5)
    results = db.search("张")
# 走出 with → 自动 close()
```

### 魔法方法调用时机

```
__init__  → 创建对象时（StudentDB() 那一刻）
__enter__ → 进入 with 时
__exit__  → 走出 with 时（自动关闭资源，推荐）
__del__   → 垃圾回收时（时间不确定，不推荐依赖）
```

---

## 6️⃣ 综合项目：MySQL 版 CLI 记账本

### 技术栈

Python + pymysql + MySQL + OOP 封装 + 上下文管理器

### 涵盖的知识点

- **OOP**：`AccountDB` 类封装所有数据库操作
- **上下文管理器**：`with` 语法自动管理连接生命周期
- **参数化查询**：所有 SQL 使用 `%s` 占位符，防注入
- **事务保证**：每次操作后 `commit()`，异常时 `rollback()`
- **数据类型**：`DECIMAL(10,2)` 存金额（不用 FLOAT，避免精度问题）
- **ENUM 类型**：`ENUM('income', 'expense')` 限制字段取值
- **COALESCE**：处理空表时 SUM() 返回 NULL 的问题
- **输入清洗**：`strip()` 去除用户输入的多余空格

### 项目功能

```
===== 记账本 =====
1. 添加记录
2. 查看所有记录
3. 按类型筛选（收入/支出）
4. 统计收支
5. 删除记录
0. 退出
```

---

## 💡 本周踩坑记录

| 坑 | 原因 | 解决方案 |
|----|------|---------|
| `(name,)` 少逗号报错 | Python 逗号才是元组标志，`(name)` 是字符串 | 始终加逗号 |
| 空表 SUM() 返回 NULL | 聚合函数对空集返回 NULL 不是 0 | 用 `COALESCE(SUM(...), 0)` |
| 浮点金额计算误差 | `FLOAT` 有精度问题（0.1+0.2≠0.3） | 用 `DECIMAL(10,2)` |
| 密码上传 GitHub | 硬编码在代码里 | `.env` + `python-dotenv` + `.gitignore` |
| 连接没关闭程序卡死 | 忘了 `close()` | `with` 语句 + `__exit__` 自动关闭 |

