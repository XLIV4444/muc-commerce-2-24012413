# 第7天学生项目：电商用户分析Web系统

## 运行方法

```bash
python -m pip install -r requirements.txt
python app.py
```

浏览器访问 `http://127.0.0.1:5000`。

- 学生用户名：`student`
- 密码：`day07`
- 教师用户名：`teacher`
- 密码：`day07`
## 上午停止线

上午只完成以下内容：

1. 建立并重命名个人项目；
2. 从VS Code终端启动Flask；
3. 测试正确登录、错误登录、访问拦截和退出；
4. 定位`app.py`、`services`、`templates`、`static`和`data`；
5. 核对已有2张指标卡、1张图和“总用户数”问答；
6. 搜索TODO，但暂不修改`TODO 2-1`至`TODO 4-1`。

## 下午核心任务

1. 检查并解释登录、退出和登录访问控制；
2. 完成4张指标卡和2张真实图表；
3. 完成偏好品类筛选；
4. 完成至少4类离线规则问答；
5. 在`screenshots`目录保存4张核心验收截图；
6. 完成一项必选拓展；
7. 修改本文件，填写个人信息、完成功能、拓展说明和未解决问题。

使用编辑器搜索`TODO`即可找到需要完成的位置。

## 必选拓展（三选一）

### A. 导出当前筛选结果

新增CSV下载功能，导出内容必须与当前`category`筛选一致。

### B. 生命周期详情页

新增`/segments`页面，展示各生命周期阶段的用户数、流失人数和流失率。

### C. Flask自动化测试

新增`tests/`目录，至少测试正确登录、未登录访问看板和`/api/ask`。

完成后必须填写下面的拓展信息，并提供`screenshots/05_extension.png`、`test_result.txt`或`tests/`测试文件作为证据。

## 学生信息

- 姓名：李昊阳	
- 学号：24012413	
- 专题方向：电商用户分析Web系统
- 已完成功能：学生手册中所有功能
- 选择的拓展任务：A,B,C
- 拓展访问或运行方法：A：网页新增CSV下载功能。B：新增`/segments`页面，展示各生命周期阶段的用户数、流失人数和流失率。C：新增`tests/`目录，测试正确登录、未登录访问看板和`/api/ask`运行方法：python -m unittest test_app -v > test_result.txt
- 拓展证据文件：screenshots，tests文件
- 尚未解决的问题：TODO
