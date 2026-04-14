
import pymysql
import random
from datetime import datetime, timedelta

# 连接数据库
conn = pymysql.connect(
    host='localhost',
    port=3306,
    user='root',
    password='1234',
    database='practice_db',
    charset='utf8mb4'
)
cursor = conn.cursor()

# 1. 创建表
cursor.execute("""
CREATE TABLE IF NOT EXISTS orders (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    product VARCHAR(100),
    amount DECIMAL(10,2),
    order_date DATE
)
""")
conn.commit()

# 2. 插入10000条模拟数据
print("正在插入10000条数据...")
products = ['键盘', '鼠标', '显示器', '耳机', '音箱', '摄像头', '麦克风', '充电器']
data = []
for i in range(10000):
    user_id = random.randint(1, 5)
    product = random.choice(products)
    amount = round(random.uniform(50, 2000), 2)
    start_date = datetime(2025, 1, 1)
    end_date = datetime(2025, 12, 31)
    random_days = random.randint(0, (end_date - start_date).days)
    order_date = start_date + timedelta(days=random_days)
    data.append((user_id, product, amount, order_date))

sql = "INSERT INTO orders (user_id, product, amount, order_date) VALUES (%s, %s, %s, %s)"
cursor.executemany(sql, data)
conn.commit()
print("数据插入完成")

# 3. 插入前EXPLAIN
print("\n" + "="*50)
print("插入前EXPLAIN（无索引）")
print("="*50)
cursor.execute("EXPLAIN SELECT * FROM orders WHERE user_id = 3")
result = cursor.fetchall()
for row in result:
    print(row)

# 4. 创建索引
print("\n创建索引 idx_user_id...")
cursor.execute("CREATE INDEX idx_user_id ON orders(user_id)")
conn.commit()

# 5. 插入后EXPLAIN
print("\n插入后EXPLAIN（有索引）")
print("="*50)
cursor.execute("EXPLAIN SELECT * FROM orders WHERE user_id = 3")
result = cursor.fetchall()
for row in result:
    print(row)

# 6. 分析对比
print("\n分析对比：")
print("无索引时：type=ALL, rows=10000（全表扫描）")
print("有索引时：type=ref, rows变小（使用索引）")

# 7. 测试索引失效
print("\n" + "="*50)
print("测试索引失效：WHERE YEAR(order_date) = 2025")
print("="*50)
cursor.execute("EXPLAIN SELECT * FROM orders WHERE YEAR(order_date) = 2025")
result = cursor.fetchall()
for row in result:
    print(row)
print("说明：对字段使用函数 YEAR() 会导致索引失效")

# 关闭连接
cursor.close()
conn.close()
print("\n全部完成！")
