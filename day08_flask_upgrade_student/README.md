# 第8天学生项目：Flask数据看板强化

## 运行方法

```bash
python -m pip install -r requirements.txt
python validate_day08_environment.py
python app.py
```

浏览器访问 `http://127.0.0.1:5000`。

- 用户名：`student`
- 密码：`day07`

## 第8天学习目标

本项目承接第7天的电商数据看板。请在原有页面、登录和问答功能基础上，完成新的路由、JSON接口、参数处理、错误响应和测试。

登录后重点测试：`/dashboard`、`/assistant`、`/health`、`/api/metrics`和`/api/categories?category=Fashion`。

## 第8天核心TODO

- `TODO 8-1`：完成`/api/metrics`指标JSON接口；
- `TODO 8-2`：完成`/api/categories`的查询参数筛选；
- `TODO 8-3`：统一400错误JSON结构；
- `TODO 8-4`：检查数据服务返回值可被`jsonify`序列化；
- 为新增接口编写至少3条Flask测试。

## 提交方式

不要新建GitHub仓库。继续使用第7天的课程仓库，在其中新增`day08_flask_upgrade/`目录，或按教师指定的第8天目录提交。提交前运行：

```bash
python validate_day08_environment.py
python validate_day08_submission.py
git status
git add day08_flask_upgrade
git diff --cached
git commit -m "完成第8天Flask项目强化"
git push
```

不要提交`.venv/`、`__pycache__/`、`.env`、真实密钥或其他缓存文件。

## 学生信息

- 姓名：李昊阳
- 学号：24012413
- 已完成路由或接口：
- 基础页面路由：`/`、`/login`、`/logout`、`/dashboard`、`/assistant`、`/segments`、`/download`

  图表图片接口：`/chart/category.png`、`/chart/order_line.png`

  问答接口：`/api/ask`

  第 8 天新增接口：`/health`、`/api/metrics`、`/api/categories`

  错误处理：400、404 统一页面 / JSON 返回

- 测试文件：`tests/test_api.py`（包含健康接口、登录拦截、指标查询、品类筛选 4 条自动化测试用例）
- 尚未解决的问题：无
