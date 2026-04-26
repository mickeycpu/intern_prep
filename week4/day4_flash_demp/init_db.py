import pymysql

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '1234',  # ← 改成你的
    'charset': 'utf8mb4',
}

# 建库
conn = pymysql.connect(**DB_CONFIG)
cursor = conn.cursor()
cursor.execute("CREATE DATABASE IF NOT EXISTS flask_demo DEFAULT CHARSET utf8mb4")
conn.commit()
cursor.close()
conn.close()

# 建表
DB_CONFIG['db'] = 'flask_demo'
conn = pymysql.connect(**DB_CONFIG)
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS students (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(50) NOT NULL,
        age INT NOT NULL,
        score DECIMAL(5,1) NOT NULL
    )
""")
conn.commit()
cursor.close()
conn.close()
print("✅ 数据库和表创建成功")
