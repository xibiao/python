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

SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DATABASE}?charset=utf8&auth_plugin_map=mysql_native_passwor"

# 邮箱配置
MAIL_SERVER = "smtp.qq.com"
MAIL_USE_SSL = True
MAIL_PORT = 465
MAIL_USERNAME = "1251511624@qq.com"
MAIL_PASSWORD = "hdzdgowvcoxdbacc"
MAIL_DEFAULT_SENDER = "1251511624@qq.com"

# session加密的盐值
SECRET_KEY = "abcdefghijklmnopqrst"


