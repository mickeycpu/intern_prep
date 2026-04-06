#  题目一 --->生成一个字典，键是1到10，值是该数字是否为偶数
s = {i:i % 2 == 0 for i in range(1,11) }
print(s)

#  题目二 --->把下面的温度（摄氏度）转换成华氏度，存成字典
cities = {"北京": 5, "上海": 12, "武汉": 10, "广州": 22}
cities2 = {city:temp * 1.8 + 32 for city,temp in cities.items()}
print(cities2)

#  题目三 --->从分数从学生成绩字典中，只保留90分以上的学生，并给每人加一个标签"优秀"列表中，只保留80分以上的，并给每人加5分
students = {"张三": 85, "李四": 92, "王五": 97, "赵六": 78, "钱七": 91}
students2 = {name:f"{score}-优秀" for name, score in students.items() if score >= 90}
print(students2)