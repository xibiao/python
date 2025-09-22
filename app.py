from flask import Flask, session, g, redirect, url_for

import config
from exts import db, mail
from models import UserModel
from flask_migrate import Migrate
# 导入蓝图
from blueprints.auth import auth_bp
from blueprints.qa import qa_bp


app = Flask(__name__)
# 绑定配置文件
app.config.from_object(config)
# 这种方式创建db会存在循环引用的问题，将db单独放在exts.py文件中创建，所有用到db的地方都从exts.py中导入
# db = SQLAlchemy(app)
db.init_app(app)
mail.init_app(app)

# flask db init  # 初始化迁移环境
# flask db migrate  # 识别ORM模型的改变，生成迁移脚本
# flask db upgrade  # 运行迁移脚本，将ORM模型改变同步到数据库中
migrate = Migrate(app, db)


# 注册蓝图
app.register_blueprint(auth_bp)
app.register_blueprint(qa_bp)


@app.before_request
def my_before_request():
    user_id = session.get('user_id')
    if user_id:
        user = UserModel.query.get(user_id)
        # setattr(g, 'user', user)
        g.user = user
    else:
        # setattr(g, 'user', None)
        g.user = None

@app.context_processor
def my_context_processor():
    return {"user": g.user}

@app.route('/')
def hello_world():  # put application's code here
    # return "hello world"
    return redirect(url_for('qa.index'))


if __name__ == '__main__':
    app.run(debug=True)
