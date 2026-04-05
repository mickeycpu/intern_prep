#  题目一
# s = [i for i  in range(1,21) if i % 2 != 0]
# print(s)

#  题目二
# words = ["hello", "world", "python", "flask"]
# words2 = [s.upper() for s in words ]
# print(words2)

#  题目三
scores = [72, 88, 95, 43, 81, 67, 90]
scores2 = [s + 5 for s in scores  if s >= 80]
print(scores2)