import pymysql
from db import DB_CONFIG

def init():
    # 建库只需要连 MySQL，不需要指定 db 名
    conn = pymysql.connect(
        host=DB_CONFIG['host'],
        user=DB_CONFIG['user'],
        password=DB_CONFIG['password'],
        charset=DB_CONFIG['charset'],
    )
    cursor = conn.cursor()

    cursor.execute("CREATE DATABASE IF NOT EXISTS rest_api_demo")
    cursor.execute("USE rest_api_demo")

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(50) NOT NULL,
            age INT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS scores (
            id INT AUTO_INCREMENT PRIMARY KEY,
            student_name VARCHAR(50) NOT NULL,
            subject VARCHAR(50) NOT NULL,
            score FLOAT NOT NULL
        )
    """)

    conn.commit()
    cursor.close()
    conn.close()
    print("✅ 数据库和表创建完成")

if __name__ == '__main__':
    init()
