Week 5 学习总结 — RESTful API + AI API接入
> 📅 学习周期：12周Python后端+AI应用开发计划 · 第5周
> 🎯 本周主题：RESTful API设计 → Flask实现 → 接口测试 → 大模型API接入 → 综合项目
> ✅ 状态：全部完成（Day 1 ~ Day 6）
---
📋 本周学习内容一览
天	主题	核心产出
Day 1	RESTful API 设计原则	API设计文档、HTTP方法与CRUD映射、统一响应格式
Day 2	Flask 实现 REST API（连接MySQL）	学生+成绩CRUD接口10个、动态搜索、分页
Day 3	Apifox 接口测试	API测试报告、错误排查实战（415/405/500）
Day 4	DeepSeek API 调用	requests调用大模型、多轮对话、OOP封装
Day 5	智谱AI API + 提示词工程	双模型客户端（策略模式）、Prompt四要素
Day 6	综合项目：AI对话接口	Flask REST API + MySQL + 双模型AI + 会话持久化
---
🧠 核心知识点
一、RESTful API 设计原则
什么是REST？
REST = Representational State Transfer，是一套API设计风格，不是协议。核心思想：URL定位资源（名词），HTTP方法定义动作（动词），各司其职。
HTTP方法与CRUD映射：
`GET` → 查（Read）：`GET /api/students` 查全部，`GET /api/students/1` 查单个
`POST` → 增（Create）：`POST /api/students` 新增
`PUT` → 改（Update）：`PUT /api/students/1` 修改id=1的记录
`DELETE` → 删（Delete）：`DELETE /api/students/1` 删除id=1的记录
URL设计规范：
只放名词（资源），用复数：`/students`，不放动词
嵌套资源用路径：`/students/1/scores`
查询参数用于过滤/分页：`/api/students?name=张&page=1&per_page=2`
统一响应格式：
```json
{
  "code": 200,
  "message": "操作成功",
  "data": { ... }
}
```
> 好处：前端写一次解析代码，所有接口通用。
HTTP状态码精要：
状态码	含义	使用场景
200	OK	通用成功（查询、修改、删除）
201	Created	新增成功
400	Bad Request	请求参数错误
401	Unauthorized	未认证（没带token）
404	Not Found	资源不存在
405	Method Not Allowed	HTTP方法不对
415	Unsupported Media Type	Content-Type不匹配
500	Internal Server Error	服务端代码bug
---
二、Flask 实现 REST API（连接MySQL）
从内存列表到数据库：
内存列表：程序关闭数据全丢，无并发安全，数据量受内存限制
MySQL：数据永久保存在磁盘，事务+行锁保证并发安全，数据量无上限
关键技术点：
```python
# lastrowid — INSERT后拿自增ID
cursor.execute("INSERT INTO students (name, age) VALUES (%s, %s)", (name, age))
conn.commit()
new_id = cursor.lastrowid

# rowcount — 判断影响行数
cursor.execute("DELETE FROM students WHERE id = %s", (id,))
affected = cursor.rowcount  # 0=没找到，1=删除成功

# 动态拼接SQL搜索（防注入）
sql = "SELECT * FROM students"
params = []
name = request.args.get('name')
if name:
    sql += " WHERE name LIKE %s"
    params.append(f"%{name}%")
cursor.execute(sql, params)
```
踩过的坑：
`conn.close()` 必须在 `return` 之前，否则连接泄漏
URL里用id不用名字：名字不唯一 + 中文编码问题
`lastrowid` 和 `rowcount` 在 `execute` 之后就准确，跟 `commit` 无关
---
三、Apifox 接口测试实战
测试中遇到的典型错误：
错误	原因	解决方案
415 Unsupported Media Type	Content-Type没设对	Apifox中Body选raw→JSON
405 Method Not Allowed	路由没定义该HTTP方法	检查`@app.route()`的`methods`列表
500 Internal Server Error	服务端代码bug	看Flask终端的traceback
关键认知：
测试通过 ≠ 返回200，预期400返回400也是通过
测试的本质是「预期 vs 实际」的对比
API调试排查顺序：服务跑起来了没 → URL对不对 → 方法对不对 → Content-Type对不对 → Body格式对不对 → 看服务端日志
---
四、大模型 API 调用
DeepSeek API 调用：
```python
import requests
from dotenv import load_dotenv
import os

load_dotenv()

url = "https://api.deepseek.com/v1/chat/completions"
headers = {
    "Authorization": f"Bearer {os.getenv('DEEPSEEK_API_KEY')}",
    "Content-Type": "application/json"
}
data = {
    "model": "deepseek-chat",
    "messages": [
        {"role": "system", "content": "你是一个Python老师"},
        {"role": "user", "content": "什么是装饰器？"}
    ]
}
response = requests.post(url, headers=headers, json=data)
reply = response.json()['choices'][0]['message']['content']
```
多轮对话原理：
AI没有记忆，每次请求都是独立的
所谓"记住上下文"是把完整对话历史每次都发过去
history列表越来越长 → token消耗越来越大 → 长对话越来越贵
双模型客户端设计（策略模式）：
```python
class DualModelClient:
    CONFIGS = {
        'deepseek': {
            'url': 'https://api.deepseek.com/v1/chat/completions',
            'model': 'deepseek-chat'
        },
        'zhipu': {
            'url': 'https://open.bigmodel.cn/api/paas/v4/chat/completions',
            'model': 'glm-4-flash'
        }
    }
    
    def __init__(self, model_name='deepseek'):
        self.model_name = model_name
        self.history = []
    
    def switch_model(self, name):
        self.model_name = name  # history保留，体验连续
    
    def _call_api(self, messages):
        # 两个模型共用一套代码，只是配置不同
        config = self.CONFIGS[self.model_name]
        ...
```
API Key安全管理：
`.env` 文件 + `python-dotenv` 读取环境变量
`.env` 加入 `.gitignore` 不上传GitHub
泄露后果：别人盗用额度、冒充身份调用
---
五、提示词工程（Prompt Engineering）
prompt四要素：
角色：AI是谁（"你是一个记账助手"）
规则：能做什么、不能做什么（"只回答记账相关问题"）
格式：输出什么格式（"不超过100字"）
风格：怎么说话（"用轻松友好的语气"）
五种常用技巧：
技巧	说明	适用场景
角色设定	限定AI行为边界	所有AI应用
Few-shot	给输入→输出示例	需要特定格式输出
Chain of Thought	让AI展示推理过程	复杂推理问题
限制条件	控制字数、限定范围	避免AI过度发挥
迭代优化	根据结果逐步调整	持续改进
---
六、综合项目：AI对话接口 `/api/chat`
项目架构：
```
Flask REST API + MySQL + 双模型AI
├── POST /api/chat          → 发消息、调AI、存历史
├── GET  /api/chat/history  → 查询会话历史
├── session_id 会话管理（UUID）
└── 对话历史持久化（MySQL chat_history表）
```
对话历史"读→用→存"三步模式：
```
load_history(session_id)  →  从数据库读历史
        ↓
client.ask(message)       →  用历史构建messages调AI
        ↓
save_message × 2          →  存用户消息 + 存AI回复
```
错误处理三层：
参数校验 → 400（message为空、请求体不是JSON）
资源不存在 → 404（session_id对应的会话不存在）
服务端异常 → 500（AI API调用失败）
函数职责单一：
`save_message()` — 只管存一条消息到数据库
`load_history()` — 只管从数据库读历史
`session_exists()` — 只管检查会话是否存在
`chat()` — 只管处理发消息请求的流程
---
🔧 本周踩过的坑
问题	原因	解决
Apifox POST请求返回415	Body类型没选JSON	Body选raw→JSON
成绩接口返回405	路由未定义POST方法	添加`methods=['POST']`
成绩查询返回500	服务端异常	看Flask终端traceback
智谱SDK安装失败	pip找不到包/版本不兼容	用requests直接调API
API返回无choices字段	Key未加载或格式错误	检查`.env`加载和Bearer格式
对话历史丢失	存在内存列表里	改用MySQL持久化存储
---
📊 本周掌握技能清单
API设计与实现：
✅ RESTful API设计原则（URL名词+HTTP方法映射）
✅ Flask实现REST API（CRUD四件套）
✅ jsonify返回JSON / 统一响应格式
✅ HTTP状态码（200/201/400/404/405/415/500）
✅ request.get_json()取JSON数据
✅ paginate()公共分页函数
✅ lastrowid / rowcount 使用
✅ 动态拼接SQL搜索（params列表防注入）
接口测试：
✅ Apifox工具使用（新建请求、设Body、发请求）
✅ Content-Type与请求体格式对应关系
✅ API测试报告编写
✅ API调试排查思维
大模型API：
✅ DeepSeek API调用（requests方式）
✅ 智谱AI API调用（requests方式）
✅ 多轮对话原理（每次发完整history）
✅ Bearer Token认证格式
✅ API Key安全管理（.env + gitignore）
✅ DeepSeekClient类封装（OOP）
✅ 双模型客户端设计（策略模式/configs字典/统一_call_api）
提示词工程：
✅ prompt四要素（角色/规则/格式/风格）
✅ Few-shot（给示例）
✅ Chain of Thought（思维链）
✅ 限制条件控制输出
✅ 迭代优化prompt
综合项目：
✅ Flask REST API + MySQL + 双模型AI综合项目
✅ 对话历史持久化（MySQL chat_history表）
✅ session_id会话管理（UUID）
✅ 对话历史"读→用→存"三步模式
✅ 错误处理三层（400/404/500）
✅ 函数职责单一原则
---
📁 本周产出文件
文件	说明
`day1_restful_api.py`	RESTful API学生+成绩管理系统：12个接口、统一响应格式、搜索分页
`day2_rest_api_mysql.py`	REST API+MySQL版：10个CRUD接口、动态搜索、分页
`day3_api_test_report.md`	Apifox API测试报告：10接口测试、错误分析
`day4_round1_basic.py`	DeepSeek API基础调用
`day4_round2_multiturn.py`	多轮对话+system角色+实时聊天
`day4_round3_oop.py`	DeepSeekClient类封装（OOP）
`day5_round1_zhipu_basic.py`	智谱AI基础调用
`day5_round2_zhipu_multiturn.py`	智谱AI多轮对话
`day5_round3_dual_client.py`	双模型客户端（DeepSeek+智谱AI切换）
`day6_ai_chat/`	Flask REST API+MySQL+双模型AI对话接口综合项目
---
🔗 相关技能栈
`Python` · `Flask` · `RESTful API` · `MySQL` · `pymysql` · `DeepSeek API` · `智谱AI API` · `Apifox` · `Prompt Engineering` · `OOP` · `Git`
---
> 📌 下一步：Week 6 — AI应用项目开发（需求分析 → 后端API → AI功能集成 → 前端页面 → 联调上线）