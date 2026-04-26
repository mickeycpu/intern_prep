import pymysql

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '1234',       # 改成你的密码
    'db': 'practice_db',
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor,
}

def get_db():
    """统一创建数据库连接"""
    return pymysql.connect(**DB_CONFIG)
