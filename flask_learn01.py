from flask import Flask, Blueprint, render_template

# 创建蓝图
learn_blueprint = Blueprint('learn', __name__, url_prefix='/learn')

# 已经在主应用程序app.py中注册此处创建的蓝图
# 运行 app.py 并尝试访问 http://127.0.0.1:5000/learn/child1
@learn_blueprint.route('/child1')
def child1():
    return render_template('extend/child1.html')

@learn_blueprint.route('/child2')
def child2():
    return render_template('extend/child2.html')

@learn_blueprint.route('/static')
def static():
    return render_template('static.html')
