# day6_account_book_cli.py
import datetime

# 1. 定义装饰器
def log_operation(func):
    def wrapper(*args, **kwargs):
        print(f"[{datetime.datetime.now()}] 操作: {func.__name__} 被调用")
        return func(*args, **kwargs)
    return wrapper

# 2. 定义核心类
class AccountBook:
    def __init__(self):
        self.balance = 0  # 当前余额
        self.records = []
        self.categories = ["餐饮", "交通", "购物", "娱乐", "工资", "其他"]

    @log_operation
    def add_income(self):
        # 实现添加收入的逻辑
        try:
            amount = float(input("请输入收入金额:"))
            if amount <= 0:
                print("金额必须大于0")
                return
        except ValueError:
            print("金额必须是数字，请重试")
            return
        category = input("请输入分类（如“工资”、“餐饮”、“交通”）:")
        if category not in self.categories:
            print(f"警告：{category} 不是预设分类，已自动添加到'其他'")
            category = "其他"

        self.balance += amount
        self.records.append((datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),"收入",amount, category))
        print("添加收入完成")

    @log_operation
    def add_expense(self):
        # 实现添加支出的逻辑
        try:
            amount = float(input("请输入支出金额:"))
            if amount <= 0:
                print("金额必须大于0")
                return
        except ValueError:
            print("金额必须是数字，请重试")
            return
        category = input("请输入分类（如“工资”、“餐饮”、“交通”）:")
        if category not in self.categories:
            print(f"警告：{category} 不是预设分类，已自动添加到'其他'")
            category = "其他"

        self.balance -= amount
        self.records.append((datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),"支出",-amount, category))
        print("添加支出完成")


    @log_operation
    def get_balance(self):
        """获取当前余额"""
        return self.balance

    @log_operation
    def get_records(self):
        """获取所有记录"""
        if not self.records:
            print("暂无记录")
            return
        print(f"\n{'时间':<18} {'类型':<6} {'金额':<8} {'分类'}")
        print("-" * 50)
        for r in self.records:
            time_r, type_r, amount_r, category_r = r
            print(f"{time_r:<18} {type_r:<6}{amount_r:<8} {category_r}")

    @log_operation
    def get_summary_by_category(self):
        """按分类统计（默认所有分类）"""
        category  =  input("请输入分类名称:")
        if category:
            filtered = [r for r in self.records if r[3] == category]
        else:
            filtered = self.records

        if not filtered:
            print(f"没有找到'{category}'的记录")
            return

        total_income = sum(r[2] for r in filtered if r[2] > 0)
        total_expense = abs(sum(r[2] for r in filtered if r[2] < 0))

        return {
            "分类": category if category else "全部",
            "总收入": total_income,
            "总支出": total_expense,
            "净收入": total_income - total_expense
        }

# 3. 主程序函数
def main():
    book = AccountBook()
    while True:
        print("\n====== 个人记账本 ======")
        print("1. 添加收入")
        print("2. 添加支出")
        print("3. 查看余额")
        print("4. 查看所有记录")
        print("5. 按分类统计")
        print("6. 退出")

        choice = input("请选择操作 (1-6): ")
        if choice == '1':
            book.add_income()
        elif choice == '2':
            book.add_expense()
        elif choice == '3':
            balance = book.get_balance()
            print(f"当前余额: {balance} 元")
        elif choice == '4':
             book.get_records()
        elif choice == '5':
            summary_by_category = book.get_summary_by_category()
            print(f"{summary_by_category}")
        elif choice == '6':
            print("感谢使用，再见！")
            break
        else:
            print("输入无效，请重新选择。")


if __name__ == "__main__":
    main()
