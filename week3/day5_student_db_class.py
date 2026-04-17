import pymysql

DB_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': '1234',
    'database': 'practice_db',
    'charset': 'utf8mb4'
}


class StudentDB:
    # ===== 第一轮 =====

    def __init__(self):
        self.conn = pymysql.connect(**DB_CONFIG)
        self.cursor = self.conn.cursor(pymysql.cursors.DictCursor)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS students (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(50),
                age INT,
                score DECIMAL(5,1)
            )
        """)
        self.conn.commit()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def insert(self, name, age, score):
        self.cursor.execute(
            "INSERT INTO students (name, age, score) VALUES (%s, %s, %s)",
            (name, age, score)
        )
        self.conn.commit()
        return self.cursor.lastrowid

    def get_by_id(self, student_id):
        self.cursor.execute("SELECT * FROM students WHERE id = %s", (student_id,))
        return self.cursor.fetchone()

    def get_all(self):
        self.cursor.execute("SELECT * FROM students")
        return self.cursor.fetchall()

    # ===== 第二轮 =====

    def insert_many(self, data):
        self.cursor.executemany(
            "INSERT INTO students (name, age, score) VALUES (%s, %s, %s)",
            data
        )
        self.conn.commit()
        return self.cursor.rowcount

    def update_score(self, student_id, new_score):
        self.cursor.execute(
            "UPDATE students SET score = %s WHERE id = %s",
            (new_score, student_id)
        )
        self.conn.commit()
        return self.cursor.rowcount > 0

    def delete(self, student_id):
        self.cursor.execute("DELETE FROM students WHERE id = %s", (student_id,))
        self.conn.commit()
        return self.cursor.rowcount > 0

    def close(self):
        self.cursor.close()
        self.conn.close()


class BookDB:
    # ===== 第三轮 =====

    def __init__(self):
        self.conn = pymysql.connect(**DB_CONFIG)
        self.cursor = self.conn.cursor(pymysql.cursors.DictCursor)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS books (
                id INT AUTO_INCREMENT PRIMARY KEY,
                title VARCHAR(100),
                author VARCHAR(50),
                price DECIMAL(8,2)
            )
        """)
        self.conn.commit()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def insert(self, title, author, price):
        self.cursor.execute(
            "INSERT INTO books (title, author, price) VALUES (%s, %s, %s)",
            (title, author, price)
        )
        self.conn.commit()
        return self.cursor.lastrowid

    def get_by_author(self, author):
        self.cursor.execute("SELECT * FROM books WHERE author = %s", (author,))
        return self.cursor.fetchall()

    def delete_by_author(self, author):
        self.cursor.execute("DELETE FROM books WHERE author = %s", (author,))
        self.conn.commit()
        return self.cursor.rowcount

    def count(self):
        self.cursor.execute("SELECT COUNT(*) FROM books")
        return self.cursor.fetchone()['COUNT(*)']

    def close(self):
        self.cursor.close()
        self.conn.close()


if __name__ == "__main__":
    # 第一轮测试
    print("===== 第一轮 =====")
    with StudentDB() as db:
        sid = db.insert("张三", 22, 85.5)
        db.insert("李四", 19, 92.0)
        print("查ID:", db.get_by_id(sid))
        print("全部:", db.get_all())

        # 第二轮测试
        print("\n===== 第二轮 =====")
        db.insert_many([
            ("王五", 25, 78.0),
            ("赵六", 21, 88.5),
        ])
        print("更新:", db.update_score(sid, 95.0))
        print("删除:", db.delete(sid))
        print("剩余:", db.get_all())
    # 走出 with → 自动调用 __exit__ → 自动 close()

    # 第三轮测试
    print("\n===== 第三轮 =====")
    with BookDB() as book_db:
        book_db.insert("三体", "刘慈欣", 35.0)
        book_db.insert("活着", "余华", 28.0)
        book_db.insert("流浪地球", "刘慈欣", 22.0)
        print("刘慈欣:", book_db.get_by_author("刘慈欣"))
        print("删除:", book_db.delete_by_author("刘慈欣"), "本")
        print("总数:", book_db.count())
    # 走出 with → 自动调用 __exit__ → 自动 close()