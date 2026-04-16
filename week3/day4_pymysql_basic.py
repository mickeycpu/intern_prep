"""
Week 3 Day 4 — pymysql 连接与基本操作
知识点：连接三层结构、CRUD、fetchone/fetchall、DictCursor、连接关闭
"""
import pymysql

DB_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': '1234',
    'database': 'practice_db',
    'charset': 'utf8mb4'
}


def get_conn():
    return pymysql.connect(**DB_CONFIG)


# ============ 第一轮：基础 CRUD ============

def create_table():
    conn = get_conn()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS students (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(50) NOT NULL,
                age INT NOT NULL,
                score DECIMAL(5, 1) NOT NULL
            )
        """)
        conn.commit()
        print("✅ students 表创建成功")
    except Exception as e:
        conn.rollback()
        print(f"❌ {e}")
    finally:
        cursor.close()
        conn.close()


def insert_one(name, age, score):
    conn = get_conn()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO students (name, age, score) VALUES (%s, %s, %s)",
            (name, age, score)
        )
        conn.commit()
        print(f"✅ 插入成功: {name}, 影响 {cursor.rowcount} 行")
    except Exception as e:
        conn.rollback()
        print(f"❌ {e}")
    finally:
        cursor.close()
        conn.close()


def query_all():
    conn = get_conn()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM students")
        rows = cursor.fetchall()
        print(f"\n📋 全部学生（共 {len(rows)} 人）:")
        for row in rows:
            print(f"  ID:{row[0]}  姓名:{row[1]}  年龄:{row[2]}  分数:{row[3]}")
        return rows
    finally:
        cursor.close()
        conn.close()


def query_by_name(name):
    conn = get_conn()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM students WHERE name = %s", (name,))
        row = cursor.fetchone()
        if row:
            print(f"🔍 找到: ID:{row[0]}  姓名:{row[1]}  年龄:{row[2]}  分数:{row[3]}")
        else:
            print(f"🔍 未找到: {name}")
        return row
    finally:
        cursor.close()
        conn.close()


def update_score(name, new_score):
    conn = get_conn()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "UPDATE students SET score = %s WHERE name = %s",
            (new_score, name)
        )
        conn.commit()
        print(f"✅ 更新 {name} 分数为 {new_score}，影响 {cursor.rowcount} 行")
    except Exception as e:
        conn.rollback()
        print(f"❌ {e}")
    finally:
        cursor.close()
        conn.close()


def delete_by_name(name):
    conn = get_conn()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM students WHERE name = %s", (name,))
        conn.commit()
        print(f"✅ 删除 {name}，影响 {cursor.rowcount} 行")
    except Exception as e:
        conn.rollback()
        print(f"❌ {e}")
    finally:
        cursor.close()
        conn.close()


# ============ 第二轮：executemany + 排序 + 统计 ============

def batch_insert(data):
    conn = get_conn()
    cursor = conn.cursor()
    try:
        cursor.executemany(
            "INSERT INTO students (name, age, score) VALUES (%s, %s, %s)",
            data
        )
        conn.commit()
        print(f"✅ 批量插入 {cursor.rowcount} 条")
    except Exception as e:
        conn.rollback()
        print(f"❌ {e}")
    finally:
        cursor.close()
        conn.close()


def query_age_gt_20_order_by_score():
    conn = get_conn()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "SELECT * FROM students WHERE age > %s ORDER BY score DESC",
            (20,)
        )
        rows = cursor.fetchall()
        print(f"\n🔍 年龄>20（按分数降序）:")
        for row in rows:
            print(f"  {row[1]}  年龄:{row[2]}  分数:{row[3]}")
        return rows
    finally:
        cursor.close()
        conn.close()


def statistics():
    conn = get_conn()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT COUNT(*), AVG(score) FROM students")
        row = cursor.fetchone()
        print(f"\n📊 统计: 总人数 {row[0]}，平均分 {row[1]:.1f}")
        return row
    finally:
        cursor.close()
        conn.close()


# ============ 第三轮：封装函数（返回字典） ============

def insert_student(name, age, score):
    conn = get_conn()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO students (name, age, score) VALUES (%s, %s, %s)",
            (name, age, score)
        )
        conn.commit()
        new_id = cursor.lastrowid
        print(f"✅ 插入成功，新 ID: {new_id}")
        return new_id
    except Exception as e:
        conn.rollback()
        print(f"❌ {e}")
        return None
    finally:
        cursor.close()
        conn.close()


def get_all_students():
    conn = get_conn()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    try:
        cursor.execute("SELECT * FROM students")
        rows = cursor.fetchall()
        print(f"\n📋 字典格式（共 {len(rows)} 人）:")
        for row in rows:
            print(f"  {row}")
        return rows
    finally:
        cursor.close()
        conn.close()


def delete_student(student_id):
    conn = get_conn()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM students WHERE id = %s", (student_id,))
        conn.commit()
        success = cursor.rowcount > 0
        if success:
            print(f"✅ ID {student_id} 删除成功")
        else:
            print(f"❌ ID {student_id} 不存在")
        return success
    except Exception as e:
        conn.rollback()
        print(f"❌ {e}")
        return False
    finally:
        cursor.close()
        conn.close()


# ============ 主程序 ============
if __name__ == "__main__":
    print("=" * 50)
    print("Week 3 Day 4 — pymysql 连接与基本操作")
    print("=" * 50)

    # 清空重建
    conn = get_conn()
    cursor = conn.cursor()
    try:
        cursor.execute("DROP TABLE IF EXISTS students")
        conn.commit()
    finally:
        cursor.close()
        conn.close()

    # 第一轮
    print("\n===== 第一轮：基础 CRUD =====")
    create_table()
    insert_one("张三", 22, 85.5)
    insert_one("李四", 19, 92.0)
    insert_one("王五", 25, 78.0)
    query_all()
    query_by_name("李四")
    query_by_name("赵六")
    update_score("张三", 90.0)
    delete_by_name("王五")
    query_all()

    # 第二轮
    print("\n===== 第二轮：批量 + 排序 + 统计 =====")
    more_data = [
        ("赵六", 21, 88.5),
        ("孙七", 23, 76.0),
        ("周八", 18, 95.0),
        ("吴九", 26, 82.0),
        ("郑十", 20, 71.5),
    ]
    batch_insert(more_data)
    query_all()
    query_age_gt_20_order_by_score()
    statistics()

    # 第三轮
    print("\n===== 第三轮：封装函数（DictCursor） =====")
    new_id = insert_student("钱十一", 24, 89.0)
    get_all_students()
    if new_id:
        delete_student(new_id)
        delete_student(999)
    get_all_students()

    print("\n✅ 全部练习完成！")
