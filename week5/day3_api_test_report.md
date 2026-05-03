# API 接口测试报告

## 项目信息
- 项目名：学生+成绩管理系统 REST API
- 测试工具：Apifox
- 测试时间：2026-04-29
- 服务地址：http://127.0.0.1:5000

## 测试结果汇总

| # | 接口 | 方法 | 预期状态码 | 实际状态码 | 结果 |
|---|------|------|-----------|-----------|------|
| 1 | /api/students | POST | 201 | 415 | ❌ |
| 2 | /api/students | GET | 200 | 200 | ✅ |
| 3 | /api/students/1 | GET | 200 | 200 | ✅ |
| 4 | /api/students/1 | PUT | 200 | 415 | ❌ |
| 5 | /api/students?name=张 | GET | 200 | 200 | ✅ |
| 6 | /api/students/1/scores | POST | 201 | 405 | ❌ |
| 7 | /api/students/1/scores | GET | 200 | 500 | ❌ |
| 8 | /api/students/999 | GET | 404 | 404 | ✅ |
| 9 | /api/students | POST | 400 | 415 | ❌ |
| 10 | /api/students/1 | DELETE | 200 | 200 | ✅ |

**通过：5/10　　失败：5/10**

## 失败接口分析

| 接口 | 错误码 | 原因分析 |
|------|--------|---------|
| POST /api/students（新增） | 415 | Content-Type 未设置为 application/json |
| PUT /api/students/1（修改） | 415 | Content-Type 未设置为 application/json |
| POST /api/students/1/scores（新增成绩） | 405 | 路由未定义该接口 |
| GET /api/students/1/scores（查成绩） | 500 | 服务端代码异常 |
| POST /api/students（缺字段） | 415 | Content-Type 未设置为 application/json |

## 结论

- GET 类查询接口和 DELETE 接口功能正常
- POST/PUT 类写入接口存在 Content-Type 配置问题（415），需在 Apifox 中将 Body 类型设置为 raw-JSON
- 成绩相关接口存在路由缺失（405）和服务端异常（500），需检查代码
