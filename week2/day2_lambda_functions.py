# day2_lambda_functions.py
# 学习目标：lambda + map / filter / sorted

# === 模拟记账本数据 ===
ledger = [
    ("2025-05-01", "餐饮", -35.5),
    ("2025-05-01", "交通", -10),
    ("2025-05-02", "工资", 8000),
    ("2025-05-03", "购物", -299),
    ("2025-05-03", "餐饮", -42),
]

# === 第1题：map 格式化 ===
formatted = list(map(lambda record: f"{record[0][5:]} {record[1]} {record[2]}", ledger))
print("格式化结果：", formatted)

# === 第2题：filter 筛选 ===
food_expenses = list(filter(lambda record: record[1] == "餐饮" and record[2] < 0, ledger))
print("餐饮支出：", food_expenses)

# === 第3题：sorted 排序 ===
sorted_by_abs = sorted(ledger, key=lambda record: abs(record[2]), reverse=True)
print("按金额绝对值排序：", sorted_by_abs)

# === 第4题：综合计算 ===
# 正确写法：map的第一个参数是函数，第二个参数是filter的结果
total_expense = sum(map(lambda r: r[2], filter(lambda r: r[2] < 0, ledger)))
print(f"本月总支出：{total_expense}")
