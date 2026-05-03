import pymysql

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '1234',
    'db': 'practice_db',
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor,
}

def get_db():
    return pymysql.connect(**DB_CONFIG)
