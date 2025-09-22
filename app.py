# pip install flask
from flask import Flask, request, render_template, make_response, json
from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
# pip install flask-migrate
from flask_migrate import Migrate

app = Flask(__name__)


# 数据库配置，集中化管理db对象‌：SQLAlchemy实例只在app.py初始化，其他模块通过导入共享
# MySQL所在的主机名
HOSTNAME = "127.0.0.1"
# MySQL监听的端口号，默认3306
PORT = 3306
# 连接MySQL的用户名和密码
USERNAME = "root"
PASSWORD = "root123"
# 连接到MySQL的哪个数据库名称
DATABASE = "mytest_python"

app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DATABASE}?charset=utf8&auth_plugin_map=mysql_native_passwor"
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# 默认True会将非ASCII字符转为Unicode编码，设置为False后保留原始UTF-8编码
app.config['JSON_AS_ASCII'] = False  # 禁用ASCII编码转换
# 在主模块app.py中创建db对象，给各个蓝图模块共享使用
db = SQLAlchemy(app)

migrate = Migrate(app, db)
# 将ORM模型映射成数据表的步骤：
# 在控制台依次执行下面三条命令，第一次需要执行三条命令，后续如果对数据表进行增删改，只需要执行2和3这两条命令。
# 1.初始化迁移环境，创建包含迁移脚本的migrations目录结构（含versions子目录和配置文件），
# 该命令仅在项目首次设置时执行一次，生成的迁移仓库会跟踪后续所有模型变更历史，形成版本控制基础框架
# flask db init  # 初始化迁移环境
# 2. 检测当前ORM模型与数据库结构的差异，自动生成包含变更操作的迁移脚本（存储在migrations/versions目录下的Python文件）
# 该步骤通过比较模型定义与数据库元数据，产生ALTER TABLE等SQL操作的Python等效代码，但不会实际修改数据库
# flask db migrate  # 识别ORM模型的改变，生成迁移脚本
# 3.执行最新迁移脚本，将挂起的模型变更同步到数据库（如新建表、添加字段等），该命令会按顺序应用所有未执行的迁移版本，
# 确保数据库结构与模型定义一致，并记录当前版本号到alembic_version表。若需回滚则可使用flask db downgrade命令
# flask db upgrade  # 运行迁移脚本，将ORM模型改变同步到数据库中


# 导入蓝图，注意：必须在db初始化后导入蓝图
from flask_learn01 import learn_blueprint
from controller.user_controller import user_blueprint
from controller.article_controller import article_blueprint

# 注册蓝图
app.register_blueprint(learn_blueprint)
app.register_blueprint(user_blueprint)
app.register_blueprint(article_blueprint)


def test_db_connection():
    # 测试数据库连接
    try:
        # 通过current_app获取应用上下文
        from flask import current_app
        with current_app.app_context():
            with db.engine.connect() as conn:
                rs = conn.execute(text("SELECT 1"))
                print("数据库连接成功:", rs.fetchone())
    except Exception as e:
        print("数据库连接失败:", str(e))

# 主应用通过@app.cli.command 确保表只初始化一次，用于执行数据库初始化等一次性任务
# Flask CLI命令‌不会自动执行‌，必须通过以下方式手动触发：在项目根目录python-flask执行 flask init-db 命令
# 注意：实际项目中不会这样使用，而是使用Migrate，通过flask db migrate/upgrade命令实现数据表的增删改
"""
@app.cli.command("init-db")
def initialize_databases():
    with app.app_context():
        test_db_connection()
        # 在主模块app.py中调用各个蓝图模块的建表方法
        create_user_table()   # 初始化用户相关表
        create_article_table()   # 初始化文章相关表
"""

# 通过after_request钩子全局设置JSON编码，通过after_request拦截器自动处理所有响应
@app.after_request
def format_response(response):
    """统一处理所有JSON响应，确保所有JSON响应使用UTF-8编码，防止中文乱码"""
    if response.content_type == 'application/json':
        # 原始响应数据转换
        data = json.loads(response.get_data())

        # 统一包装响应结构，统一错误/成功数据结构
        formatted = {
            'status': response.status_code,
            'timestamp': datetime.now().isoformat(),
            'data': data if 200 <= response.status_code < 300 else None,
            'error': data if response.status_code >= 400 else None
        }

        # 重建响应对象
        # 使用json.dumps(ensure_ascii=False)强制禁用ASCII转码，
        # 并显式设置UTF-8字符集头，解决中文乱码的问题
        response = make_response(
            json.dumps(formatted, ensure_ascii=False),
            response.status_code,
            {'Content-Type': 'application/json; charset=utf-8'}
        )
    return response


@app.route('/')
def hello_world():  # put application's code here
    # return 'Hello World 全球中心-中国欢迎您!'
    person = Person()
    dt = datetime.now()
    return render_template('index.html', username="flask", person=person, time=dt)

@app.route('/book/list')
def book_list():
    page = request.args.get('page', default=1, type=int)
    return f"你获取到的是第{page}页的图书列表。"

@app.route('/book/')
def book():
    book_list = [Book("三国演义", "罗贯中"),
             Book("水浒传", "施耐庵"),
             Book("西游记", "吴承恩"),
             Book("红楼梦", "曹雪芹")]
    return render_template('book.html', books=book_list)

# 自定义过滤器
def datetime_format(value, format='%Y-%m-%d %H:%M:%S'):
    return value.strftime(format)
# 添加过滤器，第一个参数是过滤器函数的名称，第二个参数是给这个过滤器起个名字，在其他地方通过这个名字使用这个过滤器
app.add_template_filter(datetime_format, "dateformat")


class Person:
    def __init__(self):
        self.name = "张三"
        self.age = 17

class Book:
    def __init__(self, title, author):
        self.title = title
        self.author = author


if __name__ == '__main__':
    app.run(debug=True)
