"""
Week 3 Day 6 - 综合项目：记账数据持久化（MySQL版）
将CLI记账本数据存入MySQL，实现数据持久化。

依赖：pymysql
安装：pip install pymysql
"""

import pymysql
from decimal import Decimal
from datetime import datetime


# ==================== 数据库配置 ====================
# 实际项目中应该用 .env 文件管理密码，这里为了学习简化处理
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '1234',      # ← 改成你自己的MySQL密码
    'db': 'practice_db',
    'charset': 'utf8mb4',
}


class AccountDB:
    """记账数据库操作类，封装所有MySQL操作。"""

    # 建表SQL
    CREATE_TABLE_SQL = """
    CREATE TABLE IF NOT EXISTS records (
        id INT AUTO_INCREMENT PRIMARY KEY,
        type ENUM('income', 'expense') NOT NULL,
        category VARCHAR(50) NOT NULL,
        amount DECIMAL(10,2) NOT NULL,
        note VARCHAR(200) DEFAULT '',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
    """

    def __init__(self):
        self.conn = pymysql.connect(**DB_CONFIG)
        self.cursor = self.conn.cursor(pymysql.cursors.DictCursor)
        self.cursor.execute(self.CREATE_TABLE_SQL)
        self.conn.commit()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self):
        self.cursor.close()
        self.conn.close()

    # ---- 核心方法（你需要理解每一行）----

    def add_record(self, record_type, category, amount, note=''):
        """添加一条记录。record_type: 'income' 或 'expense'"""
        sql = "INSERT INTO records (type, category, amount, note) VALUES (%s, %s, %s, %s)"
        try:
            self.cursor.execute(sql, (record_type, category, amount, note))
            self.conn.commit()
            return self.cursor.lastrowid
        except Exception as e:
            self.conn.rollback()
            print(f"添加失败：{e}")
            return None

    def get_all_records(self):
        """查询所有记录，按时间倒序。"""
        self.cursor.execute("SELECT * FROM records ORDER BY created_at DESC")
        return self.cursor.fetchall()

    def search_by_category(self, category):
        """按分类模糊查询。"""
        sql = "SELECT * FROM records WHERE category LIKE %s ORDER BY created_at DESC"
        self.cursor.execute(sql, (f"%{category}%",))
        return self.cursor.fetchall()

    def get_balance(self):
        """计算余额 = 总收入 - 总支出。"""
        sql = """
        SELECT
            COALESCE(SUM(CASE WHEN type='income' THEN amount ELSE 0 END), 0) AS total_income,
            COALESCE(SUM(CASE WHEN type='expense' THEN amount ELSE 0 END), 0) AS total_expense
        FROM records
        """
        self.cursor.execute(sql)
        row = self.cursor.fetchone()
        balance = row['total_income'] - row['total_expense']
        return {
            'total_income': row['total_income'],
            'total_expense': row['total_expense'],
            'balance': balance
        }

    def delete_record(self, record_id):
        """根据ID删除一条记录。返回是否删除成功。"""
        sql = "DELETE FROM records WHERE id = %s"
        try:
            self.cursor.execute(sql, (record_id,))
            self.conn.commit()
            return self.cursor.rowcount > 0
        except Exception as e:
            self.conn.rollback()
            print(f"删除失败：{e}")
            return False

    def get_record_by_id(self, record_id):
        """根据ID查一条记录。"""
        sql = "SELECT * FROM records WHERE id = %s"
        self.cursor.execute(sql, (record_id,))
        return self.cursor.fetchone()


# ==================== 工具函数 ====================

def input_amount(prompt="请输入金额："):
    """输入金额，必须是正数，最多两位小数。"""
    while True:
        try:
            val = input(prompt).strip()
            amount = Decimal(val)
            if amount <= 0:
                print("金额必须大于0，请重新输入。")
                continue
            if amount != amount.quantize(Decimal('0.01')):
                print("最多两位小数，请重新输入。")
                continue
            return amount
        except Exception:
            print("输入无效，请输入数字（如 50 或 99.99）。")


def print_records(records):
    """格式化打印记录列表。"""
    if not records:
        print("暂无记录。")
        return
    print(f"\n{'ID':<6}{'类型':<8}{'分类':<12}{'金额':<12}{'备注':<20}{'时间'}")
    print("-" * 70)
    for r in records:
        type_str = "收入" if r['type'] == 'income' else "支出"
        sign = "+" if r['type'] == 'income' else "-"
        print(f"{r['id']:<6}{type_str:<8}{r['category']:<12}{sign}{r['amount']:<11}{r['note']:<20}{r['created_at'].strftime('%Y-%m-%d %H:%M')}")
    print("-" * 70)


# ==================== 主菜单 ====================

def main():
    print("=" * 40)
    print("    📒 记账本 v2.0（MySQL持久化版）")
    print("=" * 40)

    with AccountDB() as db:
        while True:
            print("\n--- 主菜单 ---")
            print("1. 添加收入")
            print("2. 添加支出")
            print("3. 查看所有记录")
            print("4. 按分类查询")
            print("5. 查看余额")
            print("6. 删除记录")
            print("0. 退出")

            choice = input("\n请选择操作：").strip()

            if choice == '1':
                category = input("收入分类（如 工资/兼职/红包）：").strip()
                amount = input_amount()
                note = input("备注（可选，直接回车跳过）：").strip()
                record_id = db.add_record('income', category, amount, note)
                if record_id:
                    print(f"✅ 收入记录已添加（ID: {record_id}）")

            elif choice == '2':
                category = input("支出分类（如 吃饭/交通/购物）：").strip()
                amount = input_amount()
                note = input("备注（可选，直接回车跳过）：").strip()
                record_id = db.add_record('expense', category, amount, note)
                if record_id:
                    print(f"✅ 支出记录已添加（ID: {record_id}）")

            elif choice == '3':
                records = db.get_all_records()
                print_records(records)

            elif choice == '4':
                keyword = input("输入分类关键词：").strip()
                records = db.search_by_category(keyword)
                print_records(records)

            elif choice == '5':
                info = db.get_balance()
                print(f"\n💰 总收入：{info['total_income']}")
                print(f"💸 总支出：{info['total_expense']}")
                print(f"📊 余  额：{info['balance']}")

            elif choice == '6':
                record_id = input("输入要删除的记录ID：").strip()
                if db.delete_record(record_id):
                    print("✅ 记录已删除")
                else:
                    print("❌ 未找到该记录")

            elif choice == '0':
                print("再见！")
                break

            else:
                print("无效选择，请重新输入。")


if __name__ == '__main__':
    main()
