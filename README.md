HttpRunnerManager(已停止维护)
=================

Design Philosophy
-----------------

基于HttpRunner的接口自动化测试平台: `HttpRunner`_, `djcelery`_ and `Django`_. HttpRunner手册: http://cn.httprunner.org/

Key Features
------------

- 项目管理：新增项目、列表展示及相关操作，支持用例批量上传(标准化的HttpRunner json和yaml用例脚本)
- 模块管理：为项目新增模块，用例和配置都归属于module，module和project支持同步和异步方式
- 用例管理：分为添加config与test子功能，config定义全部变量和request等相关信息 request可以为公共参数和请求头，也可定义全部变量
- 场景管理：可以动态加载可引用的用例，跨项目、跨模快，依赖用例列表支持拖拽排序和删除
- 运行方式：可单个test，单个module，单个project，也可选择多个批量运行，支持自定义测试计划，运行时可以灵活选择配置和环境，
- 分布执行：单个用例和批量执行结果会直接在前端展示，模块和项目执行可选择为同步或者异步方式，
- 环境管理：可添加运行环境，运行用例时可以一键切换环境
- 报告查看：所有异步执行的用例均可在线查看报告，可自主命名，为空默认时间戳保存，
- 定时任务：可设置定时任务，遵循crontab表达式，可在线开启、关闭，完毕后支持邮件通知
- 持续集成：jenkins对接，开发中。。。

本地开发环境部署
--------
1. 安装mysql数据库服务端(推荐5.7+),并设置为utf-8编码，创建相应HttpRunner数据库，设置好相应用户名、密码，启动mysql

2. 修改:HttpRunnerManager/HttpRunnerManager/settings.py里DATABASES字典和邮件发送账号相关配置
   ```python
        DATABASES = {
            'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'HttpRunner',  # 新建数据库名
            'USER': 'root',  # 数据库登录名
            'PASSWORD': 'lcc123456',  # 数据库登录密码
            'HOST': '127.0.0.1',  # 数据库所在服务器ip地址
            'PORT': '3306',  # 监听端口 默认3306即可
        }
    }

    EMAIL_SEND_USERNAME = 'username@163.com'  # 定时任务报告发送邮箱，支持163,qq,sina,企业qq邮箱等，注意需要开通smtp服务
    EMAIL_SEND_PASSWORD = 'password'     # 邮箱密码
    ```
3. 安装rabbitmq消息中间件，启动服务，访问：http://host:15672/#/ host即为你部署rabbitmq的服务器ip地址
   username：guest、Password：guest, 成功登陆即可
    ```bash
        service rabbitmq-server start
    ```

4. 修改:HttpRunnerManager/HttpRunnerManager/settings.py里worker相关配置
    ```python
        djcelery.setup_loader()
        CELERY_ENABLE_UTC = True
        CELERY_TIMEZONE = 'Asia/Shanghai'
        BROKER_URL = 'amqp://guest:guest@127.0.0.1:5672//'  # 127.0.0.1即为rabbitmq-server所在服务器ip地址
        CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'
        CELERY_RESULT_BACKEND = 'djcelery.backends.database:DatabaseBackend'
        CELERY_ACCEPT_CONTENT = ['application/json']
        CELERY_TASK_SERIALIZER = 'json'
        CELERY_RESULT_SERIALIZER = 'json'

        CELERY_TASK_RESULT_EXPIRES = 7200  # celery任务执行结果的超时时间，
        CELERYD_CONCURRENCY = 10  # celery worker的并发数 也是命令行-c指定的数目 根据服务器配置实际更改 默认10
        CELERYD_MAX_TASKS_PER_CHILD = 100  # 每个worker执行了多少任务就会死掉，我建议数量可以大一些，默认100
    ```

5. 命令行窗口执行pip install -r requirements.txt 安装工程所依赖的库文件

6. 命令行窗口切换到HttpRunnerManager目录 生成数据库迁移脚本,并生成表结构
    ```bash
        python manage.py makemigrations ApiManager #生成数据迁移脚本
        python manage.py migrate  #应用到db生成数据表
    ```

7. 创建超级用户，用户后台管理数据库，并按提示输入相应用户名，密码，邮箱。 如不需用，可跳过此步骤
    ```bash
        python manage.py createsuperuser
    ```

8. 启动服务,
    ```bash
        python manage.py runserver 0.0.0.0:8000
    ```

9. 启动worker, 如果选择同步执行并确保不会使用到定时任务，那么此步骤可忽略
    ```bash
        python manage.py celery -A HttpRunnerManager worker --loglevel=info  #启动worker
        python manage.py celery beat --loglevel=info #启动定时任务监听器
        celery flower #启动任务监控后台
    ```

10. 访问：http://localhost:5555/dashboard 即可查看任务列表和状态

11. 浏览器输入：http://127.0.0.1:8000/api/register/  注册用户，开始尽情享用平台吧

12. 浏览器输入http://127.0.0.1:8000/admin/  输入步骤6设置的用户名、密码，登录后台运维管理系统，可后台管理数据

### 生产环境uwsgi+nginx部署参考：https://www.jianshu.com/p/d6f9138fab7b

新手入门手册
-----------
1、首先需要注册一个新用户,注册成功后会自动跳转到登录页面，正常登录即可访问页面
![注册页面](https://github.com/HttpRunner/HttpRunnerManager/blob/master/images/register_01.jpg)<br>
![登录页面](https://github.com/HttpRunner/HttpRunnerManager/blob/master/images/login_01.jpg)<br>

2、登陆后默认跳转到首页，左侧为菜单栏，上排有快捷操作按钮，当前只简单的做了项目，模块，用例，配置的统计
![首页](https://github.com/HttpRunner/HttpRunnerManager/blob/master/images/index_01.jpg)<br>
<br>
3、首先应该先添加一个项目，用例都是以项目为维度进行管理, 注意简要描述和其他信息可以为空, 添加成功后会自动重定向到项目列表
![新增项目](https://github.com/HttpRunner/HttpRunnerManager/blob/master/images/add_project_01.png)<br>
<br>
4、支持对项目进行二次编辑,也可以进行筛选等,项目列表页面可以选择单个项目运行，也可以批量运行，注意：删除操作会强制删除该项目下所有数据，请谨慎操作
![项目列表](https://github.com/HttpRunner/HttpRunnerManager/blob/master/images/project_list_01.jpg)<br>
<br>
5、当前项目可以新增模块了，之后用例或者配置都会归属模块下，必须指定模块所属的项目,模块列表与项目列表类似，故不赘述
![新增模块](https://github.com/HttpRunner/HttpRunnerManager/blob/master/images/add_module_01.jpg)<br>
<br>
6、新增用例，遵循HtttpRuunner脚本规范，可以跨项目，跨模块引用用例，支持拖拽排序，动态添加和删减，极大地方便了场景组织, HttpRunner用例编写很灵活，建议规范下编写方式
![新增用例01](https://github.com/HttpRunner/HttpRunnerManager/blob/master/images/add_case_01.jpg)<br>
<br>
![新增用例02](https://github.com/HttpRunner/HttpRunnerManager/blob/master/images/add_case_02.jpg)<br>
<br>
![新增用例03](https://github.com/HttpRunner/HttpRunnerManager/blob/master/images/add_case_03.jpg)<br>
<br>
![新增用例04](https://github.com/HttpRunner/HttpRunnerManager/blob/master/images/add_case_04.jpg)<br>
<br>
7、新增配置，可定义全局变量，全局hook，公共请求参数和公共headers,一般可用于测试环境，验证环境切换配置，具体用法参考HttpRunner手册
![新增配置](https://github.com/HttpRunner/HttpRunnerManager/blob/master/images/add_config_01.jpg)<br>
<br>
8、支持添加项目级别定时任务，模块集合的定时任务，遵循crontab表达式, 模块列表为空默认为整个项目，定时任务支持选择环境和配置
![添加任务](https://github.com/HttpRunner/HttpRunnerManager/blob/master/images/add_tasks_01.jpg)<br>
9、定时任务列表可以对任务进行开启或者关闭、删除，不支持二次更改
![任务列表](https://github.com/HttpRunner/HttpRunnerManager/blob/master/images/tasks_list_01.jpg)<br>
<br>
10、用例列表运行用例可以选择单个，批量运行，鼠标悬浮到用例名称后会自动展开依赖的用例，方便预览，鼠标悬浮到对应左边序列栏会自动收缩,只能同步运行
![用例列表](https://github.com/HttpRunner/HttpRunnerManager/blob/master/images/test_list_01.jpg)<br>
<br>
11、项目和模块列表可以选择单个，或者批量运行，可以选择运行环境，配置等，支持同步、异步选择，异步支持自定义报告名称，默认时间戳命名
![模块列表](https://github.com/HttpRunner/HttpRunnerManager/blob/master/images/module_list_01.jpg)<br>
<br>
12、异步运行的用例还有定时任务生成的报告均会存储在数据库，可以在线点击查看，当前不提供下载功能
![报告持久化](https://github.com/HttpRunner/HttpRunnerManager/blob/master/images/report_list_01.jpg)<br>
<br>
13、高大上的报告(基于extentreports实现), 可以一键翻转主题哦
![最终报告01](https://github.com/HttpRunner/HttpRunnerManager/blob/master/images/reports_01.jpg)<br>
<br>
![最终报告02](https://github.com/HttpRunner/HttpRunnerManager/blob/master/images/reports_02.jpg)<br>



###  其他
MockServer：https://github.com/yinquanwang/MockServer

因时间限制，平台可能还有很多潜在的bug，使用中如遇到问题，欢迎issue,
如果任何疑问好好的建议欢迎github提issue, 或者可以直接加群(628448476)，反馈会比较快












1.启动mysql数据库 service mysql start
2.启动django项目   python3 manage.py runserver 0.0.0.0:8000    
	后台启动：nohup python3 manage.py runserver 0.0.0.0:8000 >djo.out 2>&1 &   tail -f djo.out
3.启动rabittmq-server 	  docker run -d -p 15672:15672 -p 5672:5672     -e RABBITMQ_DEFAULT_USER=user     -e RABBITMQ_DEFAULT_PASS=user123     --name ct_rabbitmq     --restart always     rabbitmq:3.7-management
4.启动rabittmq-server-worker 
	python3 manage.py celery -A HttpRunnerManager worker --loglevel=info    启动worker 后台启动：nohup python3 manage.py celery -A HttpRunnerManager worker --loglevel=info  >worker.out 2>&1 &
	python3 manage.py celery beat --loglevel=info							启动定时任务监听器
	celery flower --broker=amqp://user:user123@localhost:5672//				启动任务监控后台。
	
环境搭建：
	1.首先在HttpRunnerManager的GitHub页面下载项目代码，然后存放在任意目录下。
	2.安装mysql ：root ubuntu
		查看有没有安装MySQL：dpkg -l | grep mysql
		# 安装MySQL： apt install mysql-server
		检查是否安装成功 netstat -tap | grep mysql
		初始化数据库 mysql_secure_installation
		检查mysql服务状态：systemctl status mysql
		配置mysql允许远程访问，首先编辑 /etc/mysql/mysql.conf.d/mysqld.cnf 配置文件：vim /etc/mysql/mysql.conf.d/mysqld.cnf 注释掉bind-address          = 127.0.0.1
		mysql -u root -p 授权：
			grant all on *.* to root@'%' identified by 'ubuntu' with grant option;  flush privileges;    # 刷新权限		systemctl restart mysql 重庆mysql
	3.在/HttpRunnerManager/HttpRunnerManager/修改settings.py文件里DATABASES字典的配置信息。配置mysql还有worker

	4.RabbitMQ消息中间件，由于RabbitMQ需要erlang语言的支持，在安装RabbitMQ之前需要安装erlang，再安装RabbitMQ消息中间件。
		sudo apt-get install erlang-nox
		sudo apt-get update
		sudo apt-get install rabbitmq-server
	4.1使用docker安装更佳 ：docker run -d -p 15672:15672 -p 5672:5672     -e RABBITMQ_DEFAULT_USER=user     -e RABBITMQ_DEFAULT_PASS=user123     --name ct_rabbitmq     --restart always     rabbitmq:3.7-management
		修改HttpRunnerManager/修改settings.py文件里的worker相关配置
		BROKER_URL='amqp://user:user123@localhost:5672//' if DEBUG else 'amqp://user:user123@localhost:5672//'  其中user为rabittmq服务安装指定的用户名
	
	5.切换到/HttpRunnerManager目录，使用pip3 install -r requirements.txt命令安装工程所依赖的库文件
	
	6.完成上一步后，执行python3 manage.py makemigrations ApiManager和python3 manage.py migrate命令生成数据迁移脚本并应用到db生成数据表。
	
	7.使用python3 manage.py createsuperuser命令创建超级用户，用户后台管理数据库
	
	8.使用python3 manage.py runserver 0.0.0.0:8000命令启动服务，另外如果要使用定时任务，还需要使用启动worker、启动定时任务监听器、启动任务监控后台。
	
	9.上面的服务全部启动以后，就可以通过下面的链接来访问的HttpRunnerManager服务：

    访问 http://localhost:5555/dashboard 可以查看任务列表和状态
    访问 http://127.0.0.1:8000/api/register/ 可以注册用户，开始使用平台
    访问 http://127.0.0.1:8000/admin/ 可以登录后台运维管理系统 admin Admin@123
	
	

问题记录（查看linux上httprunner包位置 pip3 show httprunner）
	1.tornado库版本==5.1.1，不然会报错
	2.status_code,headers，cookies，content等自建变量适用于extract中喝varibales，request不适用。 目前修改httprunner/response文件117行headers规则。新增req_headers和headers
	3.操作哪里的几个空白包括删除功能也无效  初步判断是CSS问题 ， 2.F12打开调试。看一下是哪个请求错误。我这边发现是amazeui.min.css， 这个css问题下载错误。http://cdn.clouddeep.cn/amazeui/1.0.1/css/amazeui.min.css
然后将这个地址替换掉templates目录下base.html中对应的地址即可。 刷新页面
	4.json数据发送单个false这种格式无法保存，解决：修改ApiManager/utils/common.py中case_info_logic函数中if request_data and data_type: 中修改and为or即可。
	5.支持文件上传
		a 修改httprunner中built_in.py和最新版httprunner中multipart_encoder方法，且pip安装filetype==1.0
		b.修改common.py文件中case_info_logic函数，新增判断data数据为{"x":"FilesOnly"}时候存入data数据为“x”到数据库
		c.修改views中edit_case函数，新增判断data数据为字符串时候，改成字典{"x":"FilesOnly"}显示在前端页面
	6.多环境下登录接口处理
		修改httprunner中client.py文件中_build_url函数中# 新增url判断，解决不同环境下登录接口地址不同问题。

	
	7.用例列表新增url显示
		a.修改项目下templates下test_list.html文件在<form class="am-form am-g" id='test_list' name="test_list">下增加一个th和一个td
		b.修改项目ApiManager\templatetags\custom_tags.py 新增convert_eval_url函数（自定义filter(过滤器):在Django模板语言中,通过使用过滤器来改变变量的显示）作用：将后台返回testcase库对象的request符串数据eval转换dict获取数据中url信息
	8.用例列表新增是否被引用
		a.修改项目ApiManager\templatetags\custom_tags.py 新增isInclude函数（过滤器）作用：判断用例对象id是否在被引用的id集合。存在返回Ture
		b.ApiManager\views 导入get_referenced_idList函数，test_list函数下新增获取被引用id列表代码并将列表传入html中
		c.修改ApiManager\utils\pagination 新增get_referenced_idList函数 作用：获取用例中被引用用例id。文件导入from django.db.models import Q # filter中不等于写法		
		d.修改项目下templates下test_list.html文件在<form class="am-form am-g" id='test_list' name="test_list">下增加一个th(是否被引用)和一个td(布尔值),td中使用过滤器显示是否被引用结果
	9.暂不支持用例名称中不支持 /
		待解决
	10.django报错invalid literal for int() with base 10: 'null‘。 原因可能是这种错误是因为模型类中某个字段的条件约束为int类型，但是给了一个字符串类型，所以报错，找到那个模型类的字段，并对应修改就好了。
		 # 暂时未找到解决办法先/usr/local/lib/python3.5/dist-packages/django/db/models/fields/__init__.py文件get_db_prep_value函数 try。except异常处理，防止django报错invalid literal for int() with base 10: 'null‘

	11.提取器value中新增支持变量($xx)来获取数据。如	content.data.content.$c.id 其中$c可以在配置中定义
		a.修改httprunner中runner.py文件中run_test函数下 # extract下 extracted_variables_mapping = resp_obj.extract_response(extractors) - >extract下 extracted_variables_mapping = resp_obj.extract_response(extractors,context=self.context)
		作用：在提取器中传入用例的context上下文，在后续函数中通过content获取变量值
		b.修改httprunner中response.py文件中extract_response函数，新增默认参数context=""，将context形参传入extract_field函数中
		  修改httprunner中response.py文件中extract_field函数，新增默认参数context=""，将context形参传入_extract_field_with_delimiter函数中
		  修改httprunner中response.py文件中_extract_field_with_delimiter函数，新增默认参数context=""，将context形参传入# response body下utils.query_json中
		  修改httprunner中utils文件中query_json函数新增默认参数context=""，修改处理逻辑：判断query列表中是否存在变量（import testcase 适用testcase.extract_variables()方法）。如果是变量就通过context参数的
		  testcase_parser.get_bind_variable()方法获取变量对应值，在将值给key。
	
	12.去除首页百度地图API弹框提示问题
		a.修改HttpRunnerManager/templates/index.html文件中39行百度api的js去除
		  
	13.报告页面显示问题，HttpRunnerManager\templates\和report_template.html中该JS无法访问 http://extentreports.com/resx/dist/js/extent.js和 xxxx.css
		a.下载css和js到本地static下assets下js/css目录下。更新两个html文件中js和css引用(下载地址：https://github.com/anshooarora/extentreports-java/tree/master/dist)
		b.在html加入{% load staticfiles %} 表示：加载静态资源。导入css：    <link href='{% static 'assets/css/extent.css' %}' type='text/css' rel='stylesheet'/> 导入js:   <script src="{% static 'assets/js/extent.js' %}"></script>
	13.1.异步运行生成报告无样式问题。
		a.异步运行调用的是extent_report_template.html模板，且jinja2(异步运行适用jinja2.templates实现将数据转化为html文件)的templates模板语法和django的的一些语法有冲突（无法识别{%load staticfile%}等语法）。故直接将extent.js和ext
		ent.css内容写入到extent_report_template.html文件中。
		
	14.为空的用例支持检验断言（目前暂未提交到服务器）
		a.修改HttpRunnerManager\ApiManager\utils\runner文件中run_by_single函数下76航，注释url不为空加入testcase_list逻辑。
		b.修改httprunner库下client文件_build_url函数，增加判断  if path == "":return False   request函数中新增判断  if url==False:response = None return response
	 
	15.首页图表显示缺失：
		原因：index.html中引用的echarts的js网址无法访问了
		修改：注释之前的对echarts引用。改用：<script src="https://cdnjs.cloudflare.com/ajax/libs/echarts/4.3.0/echarts.min.js"></script>  （引用网址：https://cdnjs.com/libraries/echarts）
		
		

		
