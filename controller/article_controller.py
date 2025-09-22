from flask import Blueprint, jsonify, request
from werkzeug.exceptions import BadRequest

from app import db  # 从主模块导入共享的db对象
from utils.serializers import model_to_dict

# 创建蓝图
article_blueprint = Blueprint('article', __name__)

# 注意：模型定义必须在创建db对象之后，在主模块app.py中创建了db对象，需要从主模块导入共享的db对象
class Article(db.Model):
    __tablename__ = "t_python_article"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(20), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('t_python_user.id'), nullable=False)
    # 若使用back_populates建立Article与User之间的关联关系，则在Article与User类中都需要定义相关联的属性，如下所示
    # articles = db.relationship('Article', back_populates='author') # 在User类中定义的关联属性
    # author = db.relationship('User', back_populates='articles') # 在Article类中定义的关联属性
    # backref 会自动给User模型添加一个articles属性，用于获取文章列表
    # 对于复杂关系场景，建议使用back_populates替代backref以获得更明确的映射控制
    # lazy='dynamic'只适用于一对多或多对多关系，不适用于多对一或一对一的关系
    author = db.relationship('User', backref='articles')


# 每个蓝图模块维护自己的模型和建表方法，在主模块app.py中调用各个蓝图模块的建表方法
def create_article_table():
    try:
        # 通过current_app获取应用上下文
        from flask import current_app
        with current_app.app_context():
            db.create_all()
            print("创建数据表成功")
    except Exception as e:
        print("创建数据表失败：", str(e))


# 正确的蓝图路由‌：使用@blueprint_name.route而非@app.route，否则找不到接口
# 创建文章，使用postman发起POST请求：http://127.0.0.1:5000/article/add
"""
请求体：
{
    "title": "三国演义",
    "content": "《三国演义》是元末明初小说家罗贯中创作的长篇章回体历史演义小说",
    "author_id": 1
}
"""
@article_blueprint.route("/article/add", methods=["POST"])
def add_article():
    try:
        data = request.get_json()
        if not all(k in data for k in ['title', 'content', 'author_id']):
            raise BadRequest("Missing required fields")

        article = Article(
            title=data['title'],
            content=data['content'],
            author_id=data['author_id']
        )
        db.session.add(article)
        db.session.commit()
        return model_to_dict(article)
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@article_blueprint.route("/article/query_by_author/<author_id>", methods=["GET"])
def query_by_author(author_id):
    try:
        articles = Article.query.filter_by(author_id = author_id).all()
        return [model_to_dict(article) for article in articles]  # 列表推导式处理
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# 测试用例
def test_add_article():
    # 通过current_app获取应用上下文
    from flask import current_app
    with current_app.test_client() as client:
        resp = client.post(
            '/article/add',
            json={
                'title': '测试文章',
                'content': '测试内容',
                'author_id': 1
            }
        )
        assert resp.status_code == 200
        assert resp.json['title'] == '测试文章'

if __name__ == '__main__':
    test_add_article()

