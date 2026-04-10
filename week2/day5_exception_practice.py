def get_positive_number():
    while True:
        try:
            num = int(input("请输入一个正数: "))
            if num > 0:  # 正数必须大于0
                print(f"输入成功！您输入的数字是: {num}")
                return num  # 返回有效的正数
            else:
                print("请输入大于0的正数！")
        except ValueError:
            print("输入无效，请输入数字！")

if __name__ == "__main__":
    result = get_positive_number()
    print(f"函数返回值: {result}")
