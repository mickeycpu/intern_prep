import pymysql

conn = pymysql.connect(
    host="localhost",
    port=3306,
    user="root",
    password="1234",
    database="intern_prep",
    charset="utf8mb4"
)

cursor = conn.cursor()

print("=== 查询所有学生 ===")
cursor.execute("SELECT * FROM students")
for row in cursor.fetchall():
    print(row)

print("\n=== 插入孙九 ===")
sql = "INSERT INTO students (name, score) VALUES (%s, %s)"
cursor.execute(sql, ("孙九", 76))

conn.commit()
print("插入成功")

print("\n=== 修改孙九分数为95 ===")
sql = "UPDATE students SET score = %s WHERE name = %s"
cursor.execute(sql, (95, "孙九"))
conn.commit()
print("修改成功")

print("\n=== 删除孙九 ===")
sql = "DELETE FROM students WHERE name = %s"
cursor.execute(sql, ("孙九",))
conn.commit()
print("删除成功")

print("\n=== 最终数据 ===")
cursor.execute("SELECT * FROM students")
for row in cursor.fetchall():
    print(row)

cursor.close()
conn.close()
