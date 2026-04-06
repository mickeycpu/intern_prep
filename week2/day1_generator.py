# 生成器练习：生成1到n之间的所有偶数

def even_numbers(n):
    """生成器：yield 1到n之间的偶数"""
    for i in range(1, n + 1):    # 遍历 1 到 n
        if i % 2 == 0:           # 如果是偶数
            yield i              # 返回这个偶数，然后暂停

# for 循环会自动调用 next() 直到生成器耗尽
for num in even_numbers(10):
    print(num)

# 输出: 2 4 6 8 10



# 生成器表达式：生成器的简写形式

# 列表推导式：立刻生成所有值，存进内存
nums_list = [x * 2 for x in range(10)]
print(nums_list)    # [0, 2, 4, 6, 8, 10, 12, 14, 16, 18]

# 生成器表达式：用到才生成，省内存
nums_gen = (x * 2 for x in range(10))
print(nums_gen)     # <generator object ...>

# 生成器表达式可以用 for 循环遍历
for n in (x * 2 for x in range(10)):
    print(n, end=" ")
print()  # 输出: 0 2 4 6 8 10 12 14 16 18

# 区别：列表推导式用 []，生成器表达式用 ()
