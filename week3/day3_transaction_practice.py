import pymysql

def get_connection():
    return pymysql.connect(
        host='localhost',
        user='root',
        password='1234',  # ← 改成你自己的
        database='test',       # ← 改成你自己的库名
        charset='utf8mb4'
    )


def transfer(from_name, to_name, amount):
    """事务转账：from 给 to 转 amount 元"""
    conn = get_connection()
    cursor = conn.cursor()

    try:
        # 1. 检查余额是否充足
        cursor.execute("SELECT balance FROM accounts WHERE name = %s", (from_name,))
        result = cursor.fetchone()
        if result is None:
            print(f"账户 {from_name} 不存在")
            return False
        if float(result[0]) < amount:
            print(f"余额不足！{from_name} 当前余额: {result[0]}，要转: {amount}")
            return False

        # 2. 扣款 + 加款（事务包裹）
        cursor.execute(
            "UPDATE accounts SET balance = balance - %s WHERE name = %s",
            (amount, from_name)
        )
        cursor.execute(
            "UPDATE accounts SET balance = balance + %s WHERE name = %s",
            (amount, to_name)
        )

        # 3. 全部成功，提交
        conn.commit()
        print(f"转账成功：{from_name} → {to_name}，金额：{amount}")
        return True

    except Exception as e:
        # 4. 出错，回滚
        conn.rollback()
        print(f"转账失败，已回滚：{e}")
        return False

    finally:
        cursor.close()
        conn.close()


def batch_insert_users(data_list):
    """批量插入用户：executemany"""
    conn = get_connection()
    cursor = conn.cursor()

    try:
        sql = "INSERT INTO accounts (name, balance) VALUES (%s, %s)"
        cursor.executemany(sql, data_list)
        conn.commit()
        print(f"批量插入成功，插入了 {cursor.rowcount} 条数据")

    except Exception as e:
        conn.rollback()
        print(f"批量插入失败，已回滚：{e}")

    finally:
        cursor.close()
        conn.close()


def show_all():
    """查看所有账户余额"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, balance FROM accounts")
    rows = cursor.fetchall()
    print("\n--- 当前账户 ---")
    for row in rows:
        print(f"  ID:{row[0]}  姓名:{row[1]}  余额:{row[2]}")
    print()
    cursor.close()
    conn.close()
