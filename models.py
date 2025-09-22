from datetime import datetime

from exts import db

class UserModel(db.Model):
    __tablename__ = 't_python_flask_user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(30), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(30), nullable=False, unique=True)
    join_time = db.Column(db.DateTime, nullable=False, default=datetime.now)


class EmailCaptchaModel(db.Model):
    __tablename__ = 't_python_flask_email_captcha'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(30), nullable=False)
    captcha = db.Column(db.String(10), nullable=False)
    create_time = db.Column(db.DateTime, nullable=False, default=datetime.now)


class QuestionModel(db.Model):
    __tablename__ = 't_python_flask_question'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.DateTime, nullable=False, default=datetime.now)

    # 外键
    author_id = db.Column(db.Integer, db.ForeignKey('t_python_flask_user.id'), nullable=False)
    # 若使用 back_populates 建立 QuestionModel 与 UserModel 之间的关联关系，
    # 则在 QuestionModel 与 UserModel 类中都需要定义相关联的属性，如下所示
    # questions = db.relationship('QuestionModel', back_populates='author') # 在UserModel类中定义的关联属性
    # author = db.relationship('UserModel', back_populates='questions') # 在QuestionModel类中定义的关联属性
    # backref 会自动给UserModel模型添加一个questions属性，用于获取问答列表
    # 对于复杂关系场景，建议使用back_populates替代backref以获得更明确的映射控制
    # lazy='dynamic'只适用于一对多或多对多关系，不适用于多对一或一对一的关系
    author = db.relationship('UserModel', backref='questions')


class AnswerModel(db.Model):
    __tablename__ = 't_python_flask_answer'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.DateTime, nullable=False, default=datetime.now)

    # 定义外键
    question_id = db.Column(db.Integer, db.ForeignKey('t_python_flask_question.id'), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('t_python_flask_user.id'), nullable=False)
    # 定义关联关系
    question = db.relationship('QuestionModel', backref=db.backref('answers', order_by=create_time.desc()))
    author = db.relationship('UserModel', backref='answers')


