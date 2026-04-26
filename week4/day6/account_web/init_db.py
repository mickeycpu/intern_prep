"""建表脚本 — 运行一次即可"""
import pymysql

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': input('请输入MySQL密码: '),
    'charset': 'utf8mb4',
}

DB_NAME = 'practice_db'


def init_db():
    conn = pymysql.connect(**DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME} DEFAULT CHARSET utf8mb4")
    conn.commit()
    cursor.close()
    conn.close()

    DB_CONFIG['db'] = DB_NAME
    conn = pymysql.connect(**DB_CONFIG)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS records (
            id INT AUTO_INCREMENT PRIMARY KEY,
            type ENUM('income', 'expense') NOT NULL,
            category VARCHAR(50) NOT NULL,
            amount DECIMAL(10,2) NOT NULL,
            note VARCHAR(200) DEFAULT '',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()

    cursor.execute("SELECT COUNT(*) FROM records")
    if cursor.fetchone()[0] == 0:
        sample = [
            ('expense', '餐饮', 35.00, '午饭'),
            ('expense', '交通', 15.00, '地铁'),
            ('income', '工资', 5000.00, '4月工资'),
            ('expense', '购物', 200.00, '买衣服'),
        ]
        cursor.executemany(
            "INSERT INTO records (type, category, amount, note) VALUES (%s, %s, %s, %s)",
            sample
        )
        conn.commit()
        print(f"✅ 已插入 {len(sample)} 条示例数据")

    cursor.close()
    conn.close()
    print(f"✅ 数据库 `{DB_NAME}` 和 `records` 表创建完成")


if __name__ == '__main__':
    init_db()
