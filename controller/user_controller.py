from flask import Blueprint, jsonify, request
from werkzeug.security import generate_password_hash
from app import db  # 从主模块导入共享的db对象

from utils.serializers import model_to_dict


# 创建蓝图
user_blueprint = Blueprint('user', __name__)
# user_blueprint = Blueprint('user', __name__, url_prefix='/db')

# 移除重复的Flask实例，各模块只需维护蓝图对象，只有主模块app.py才需要创建Flask对象
# app = Flask(__name__)

# 注意：模型定义必须在创建db对象之后，在主模块app.py中创建了db对象，需要从主模块导入共享的db对象
class User(db.Model):
    __tablename__ = "t_python_user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(20), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    # 若使用 back_populates 建立Article与User之间的关联关系，则在Article与User类中都需要定义相关联的属性，如下所示
    # articles = db.relationship('Article', back_populates='author') # 在User类中定义的关联属性
    # author = db.relationship('User', back_populates='articles') # 在Article类中定义的关联属性
    # articles = db.relationship('Article', backref='author', lazy='dynamic')

    def __init__(self, name, password):
        self.name = name
        self.password = password

    # 创建序列化方法，将模型对象转成字符串
    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


# 每个蓝图模块维护自己的模型和建表方法，在主模块app.py中调用各个蓝图模块的建表方法
def create_user_table():
    try:
        # 通过current_app获取应用上下文
        from flask import current_app
        with current_app.app_context():
            db.create_all()
            print("创建数据表成功")
    except Exception as e:
        print("创建数据表失败：", str(e))


# 正确的蓝图路由‌：使用@blueprint_name.route而非@app.route，否则找不到接口
# 创建用户
@user_blueprint.route("/user/add")
def add_user():
    try:
        users = []
        # 1.创建ORM对象
        users.append(User(name="admin", password="123456"))
        users.append(User(name="张三", password="111111"))
        users.append(User("张三丰", "333333"))
        # 2.将ORM对象添加到db.session中
        for user in users:
            db.session.add(user)
        # 3.将db.session中的数据提交到数据库中
        db.session.commit()
        return jsonify({"status": "success"})
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# 查询用户
@user_blueprint.route("/user/query/<id>")
def query_user(id):
    try:
        user = User.query.get(id)
        if user is None:
            # 使用 make_response 确保状态码和头部正确传递
            return {"error": f"用户不存在 {id}"}, 404
            # return "用户不存在"
        return jsonify(user.to_dict())
    except Exception as e:
        return {"error": str(e)}, 500

@user_blueprint.route("/user/filter/<param>")
def filter_user(param):
    try:
        """
        user = User.query.filter_by(User.name == param).first()
        # user = User.query.filter_by(name = param).first()
        if user is None:
            return {"error": f"用户不存在 {id}"}, 404
        return jsonify(user.to_dict())
        """
        users = User.query.filter(User.name == param).all()
        users_data = [model_to_dict(user, excludes=['password']) for user in users]
        return jsonify(users_data)
    except Exception as e:
        return {"error": str(e)}, 500

# 浏览器发送get请求：http://127.0.0.1:5000/user/update/4?name=李四&password=222
@user_blueprint.route("/user/update/<id>")
def update_user(id):
    try:
        user = User.query.get(id)
        if user is None:
            return {"error": f"用户不存在 {id}"}, 404
        name = request.args.get('name')
        if name is None:
            raise Exception("参数错误")
        user.name = name
        password = request.args.get('password')
        if password is not None:
            # user.password = generate_password_hash(password)
            user.password = password
        db.session.commit()
        # return jsonify(user.to_dict())
        return jsonify(model_to_dict(user, excludes=['password']))
    except Exception as e:
        return {"error": str(e)}, 500


@user_blueprint.route("/user/delete/<id>")
def delete_user(id):
    try:
        user = User.query.get(id)
        if user is None:
            return {"error": f"用户不存在 {id}"}, 404
        db.session.delete(user)
        db.session.commit()
        return jsonify({"status": "success"})
    except Exception as e:
        return {"error": str(e)}, 500


# 通过PUT方式修改数据
@user_blueprint.route("/user/modify/<int:id>", methods=['PUT'])
def modify_user(id):
    try:
        # 参数校验
        if not request.is_json:
            return {"error": "请求必须为JSON格式"}, 400

        data = request.get_json()
        required_fields = ['name', 'password']
        if not all(field in data for field in required_fields):
            return {"error": "缺少必要参数"}, 400

        # 业务逻辑
        user = User.query.get(id)
        if not user:
            return {"error": f"用户不存在 {id}"}, 404

        # 密码加密存储
        user.name = data['name']
        user.password = generate_password_hash(data['password'])  # 使用密码哈希
        db.session.commit()

        # 安全返回
        return jsonify(user.to_dict())

    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 500

