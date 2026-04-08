# day3_account_book.py
# Day 3: 面向对象基础 - 记账本类

class AccountBook:
    """记账本类"""

    def __init__(self):
        """初始化记账本"""
        self.balance = 0      # 当前余额
        self.records = []     # 记录列表，每个元素是(日期, 类型, 金额, 分类, 备注)
        self.categories = ["餐饮", "交通", "购物", "娱乐", "工资", "其他"]

    def add_income(self, amount, category, date, note=""):
        """添加收入"""
        if category not in self.categories:
            print(f"警告：{category} 不是预设分类，已自动添加到'其他'")
            category = "其他"

        self.balance += amount
        self.records.append((date, "收入", amount, category, note))
        print(f"✅ 收入 {amount} 元（{category}），当前余额 {self.balance}")

    def add_expense(self, amount, category, date, note=""):
        """添加支出"""
        if category not in self.categories:
            print(f"警告：{category} 不是预设分类，已自动添加到'其他'")
            category = "其他"

        self.balance -= amount
        self.records.append((date, "支出", -amount, category, note))
        print(f"❌ 支出 {amount} 元（{category}），当前余额 {self.balance}")

    def get_balance(self):
        """获取当前余额"""
        return self.balance

    def get_records(self):
        """获取所有记录"""
        return self.records

    def get_summary_by_category(self, category=None):
        """按分类统计（默认所有分类）"""
        if category:
            filtered = [r for r in self.records if r[3] == category]
        else:
            filtered = self.records

        total_income = sum(r[2] for r in filtered if r[2] > 0)
        total_expense = abs(sum(r[2] for r in filtered if r[2] < 0))

        return {
            "分类": category if category else "全部",
            "总收入": total_income,
            "总支出": total_expense,
            "净收入": total_income - total_expense
        }

# === 测试代码 ===
if __name__ == "__main__":
    # 创建记账本
    my_book = AccountBook()

    # 添加收入
    my_book.add_income(5000, "工资", "2025-05-01", "5月工资")
    my_book.add_income(200, "其他", "2025-05-05", "红包")

    # 添加支出
    my_book.add_expense(35.5, "餐饮", "2025-05-01", "午饭")
    my_book.add_expense(299, "购物", "2025-05-03", "耳机")

    # 查看余额
    print(f"\n当前余额：{my_book.get_balance()}")

    # 查看所有记录
    print("\n所有记录：")
    for record in my_book.get_records():
        print(f"  {record}")

    # 按分类统计
    print("\n分类统计：")
    print(my_book.get_summary_by_category("餐饮"))
    print(my_book.get_summary_by_category())
