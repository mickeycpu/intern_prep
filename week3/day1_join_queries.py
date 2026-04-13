import pymysql

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

# 查询1：每个用户的所有订单（INNER JOIN）
print('=' * 50)
print('查询1：每个用户的所有订单（INNER JOIN）')
print('=' * 50)
sql1 = """
SELECT users.name, orders.product, orders.amount
FROM users
INNER JOIN orders ON users.id = orders.user_id
"""
cursor.execute(sql1)
for row in cursor.fetchall():
    print(row)


# 查询2：所有用户及其订单，没订单的也显示（LEFT JOIN）
print('=' * 50)
print('查询2：所有用户及其订单（LEFT JOIN）')
print('=' * 50)
sql2 = """
SELECT users.name, orders.product, orders.amount
FROM users
LEFT JOIN orders ON users.id = orders.user_id
"""
cursor.execute(sql2)
for row in cursor.fetchall():
    print(row)


# 查询3：每个用户的总消费金额，按金额降序
print('=' * 50)
print('查询3：每个用户的总消费金额（GROUP BY + SUM）')
print('=' * 50)
sql3 = """
SELECT users.name, SUM(orders.amount) AS total
FROM users
LEFT JOIN orders ON users.id = orders.user_id
GROUP BY users.name
ORDER BY total DESC
"""
cursor.execute(sql3)
for row in cursor.fetchall():
    print(row)


# 查询4：消费金额最高的用户
print('=' * 50)
print('查询4：消费金额最高的用户')
print('=' * 50)
sql4 = """
SELECT users.name, SUM(orders.amount) AS total
FROM users
INNER JOIN orders ON users.id = orders.user_id
GROUP BY users.name
ORDER BY total DESC
LIMIT 1
"""
cursor.execute(sql4)
for row in cursor.fetchall():
    print(row)


# 查询5：没有下过单的用户
print('=' * 50)
print('查询5：没有下过单的用户')
print('=' * 50)
sql5 = """
SELECT users.name
FROM users
LEFT JOIN orders ON users.id = orders.user_id
WHERE orders.id IS NULL
"""
cursor.execute(sql5)
for row in cursor.fetchall():
    print(row)


# 查询6：每个城市的用户数量和总消费金额
print('=' * 50)
print('查询6：每个城市的用户数量和总消费金额')
print('=' * 50)
sql6 = """
SELECT
    users.city,
    COUNT(DISTINCT users.id) AS user_count,
    IFNULL(SUM(orders.amount), 0) AS city_total
FROM users
LEFT JOIN orders ON users.id = orders.user_id
GROUP BY users.city
"""
cursor.execute(sql6)
for row in cursor.fetchall():
    print(row)


# 关闭连接
cursor.close()
conn.close()
print('=' * 50)
print('全部查询完成')
