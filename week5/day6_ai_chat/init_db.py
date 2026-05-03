import pymysql

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '你的密码',
    'charset': 'utf8mb4',
}

# 先建数据库
conn = pymysql.connect(**DB_CONFIG)
cursor = conn.cursor()
cursor.execute("CREATE DATABASE IF NOT EXISTS ai_chat DEFAULT CHARSET utf8mb4")
conn.commit()
cursor.close()
conn.close()

# 再建表（连到 ai_chat 库）
DB_CONFIG['db'] = 'ai_chat'
conn = pymysql.connect(**DB_CONFIG)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS chat_history (
    id INT AUTO_INCREMENT PRIMARY KEY,
    session_id VARCHAR(64) NOT NULL,
    role ENUM('user', 'assistant') NOT NULL,
    content TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_session_id (session_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
""")

conn.commit()
print("✅ 数据库 ai_chat 和表 chat_history 创建成功")
cursor.close()
conn.close()
