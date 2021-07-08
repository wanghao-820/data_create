### 简介
* 定义非必要参数，快捷构造测试数据


### 目前支持（使用方法见 sample.py）
* 注册新账号（随机手机号，姓名）
* 创建课程
* 创建课时
* 创建小班
* 课堂表现数据
* 正转正绩效数据构造和验证
* 内部报班
* 落地页报班
* 9元分班逻辑验证脚本

### 项目结构说明
* apis: 后端接口, 保留所有的传参
* controllers: 接口的封装，无需关心的参数都在此处定义。只保留最核心参数供外部调用
* utils: 各种公用方法的实现
### base on :
* python3.6 +
* requests(pip install requests)
* pymysql (pip install pymysql)
* redis (pip install redis)
* Faker （pip install Faker）
* jsondiff (pip install jsondiff)
