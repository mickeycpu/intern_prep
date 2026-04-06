# 装饰器基础：@语法糖

def my_decorator(func):
    """装饰器：在原函数执行前后各加一行打印"""
    def wrapper():
        print("开始执行...")    # 原函数执行前
        func()                  # 执行原函数
        print("执行结束")       # 原函数执行后
    return wrapper

@my_decorator
def say_hello():
    print("你好！")

@my_decorator
def say_bye():
    print("再见！")

# 调用时实际执行的是 wrapper()
say_hello()
print("---")
say_bye()



# 装饰器传参：*args 和 **kwargs

def my_decorator(func):
    """装饰器：支持任意参数"""
    def wrapper(*args, **kwargs):
        # *args   = 收集位置参数，打包成元组
        # **kwargs = 收集关键字参数，打包成字典
        print("调用前")
        result = func(*args, **kwargs)  # 原封不动传给原函数
        print("调用后")
        return result                   # 原封不动返回原函数的结果
    return wrapper

@my_decorator
def add(a, b):
    return a + b

@my_decorator
def greet(name):
    return f"你好，{name}"

print(add(3, 5))        # 输出: 调用前 调用后 8
print("---")
print(greet("张添宇"))  # 输出: 调用前 调用后 你好，张添宇



# 实用装饰器：计算函数执行时间

import time

def timer(func):
    """计时装饰器：自动打印函数执行耗时"""
    def wrapper(*args, **kwargs):
        start = time.time()                 # 记录开始时间
        result = func(*args, **kwargs)      # 执行原函数
        end = time.time()                   # 记录结束时间
        print(f"{func.__name__} 执行耗时: {end - start:.4f} 秒")
        return result
    return wrapper

@timer
def slow_add(a, b):
    time.sleep(1)    # 模拟耗时1秒
    return a + b

@timer
def slow_multiply(a, b):
    time.sleep(2)    # 模拟耗时2秒
    return a * b

print(slow_add(3, 5))
print("---")
print(slow_multiply(3, 5))



# 生成器基础：yield 的工作原理

def test():
    """演示 yield 的暂停特性"""
    print("第1步")
    yield 1         # 返回1，暂停
    print("第2步")
    yield 2         # 返回2，暂停
    print("第3步")
    yield 3         # 返回3，暂停

gen = test()        # 创建生成器对象，此时还没执行任何代码

# 每次 next() 从上次暂停的地方继续
print(next(gen))    # 执行到第1个yield，输出: 第1步  1
print(next(gen))    # 执行到第2个yield，输出: 第2步  2
print(next(gen))    # 执行到第3个yield，输出: 第3步  3

# yield 的本质：暂停 + 返回值，下次调用从暂停处继续



