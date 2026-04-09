class Student:
    def __init__(self, name):
        self.name = name          # 公有属性：姓名
        self.__scores = []        # 私有属性：成绩列表（用复数更合理）

    def add_score(self, score):
        """添加成绩，验证0-100"""
        if 0 <= score <= 100:
            self.__scores.append(score)
            return f"添加成绩 {score} 成功"
        else:
            return "成绩必须在0-100之间"

    def get_average(self):
        """计算平均分"""
        if not self.__scores:  # 如果成绩列表为空
            return 0
        total = sum(self.__scores)
        return total / len(self.__scores)

    def get_scores(self):
        """返回成绩列表的副本（防止外部修改）"""
        return self.__scores.copy()

    def show_info(self):
        """显示学生信息"""
        return f"姓名：{self.name}，成绩列表：{self.__scores}，平均分：{self.get_average():.1f}"


# === 测试代码 ===
if __name__ == "__main__":
    # 创建学生实例
    student = Student("张三")

    # 添加成绩
    print(student.add_score(85))
    print(student.add_score(92))
    print(student.add_score(78))
    print(student.add_score(150))  # 测试验证：超过100

    # 显示信息
    print("\n" + student.show_info())

    # 获取成绩列表（副本）
    scores = student.get_scores()
    print(f"成绩列表：{scores}")

    # 尝试修改副本（不影响原数据）
    scores.append(999)
    print(f"修改后的副本：{scores}")
    print(f"原始成绩列表（不受影响）：{student.get_scores()}")
