from db import get_db

conn = get_db()
cursor = conn.cursor()

# 学生表
cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    age INT,
    score DECIMAL(5,2)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
""")

# 课程表
cursor.execute("""
CREATE TABLE IF NOT EXISTS courses (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    teacher VARCHAR(50),
    hours INT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
""")

conn.commit()
cursor.close()
conn.close()
print("✅ students 表 + courses 表创建完成")
