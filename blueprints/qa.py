from flask import Blueprint, render_template, redirect, url_for, request, g

from blueprints.forms import QuestionForm, AnswerForm
from exts import db
from decorators import login_required
from models import QuestionModel, AnswerModel

# 创建蓝图
qa_bp = Blueprint('qa', __name__, url_prefix='/qa')


@qa_bp.route('/')
@login_required  # 若未登录，则需要先登录
def index():
    questions = QuestionModel.query.order_by(QuestionModel.create_time.desc()).all()
    return render_template("index.html", questions=questions)


@qa_bp.route('/public', methods=['GET', 'POST'])
@login_required
def public_question():
    if request.method == 'GET':
        return render_template('public_question.html')
    else:
        form = QuestionForm(request.form)
        if form.validate():
            title = form.title.data
            content = form.content.data
            question = QuestionModel(title=title, content=content, author = g.user)
            db.session.add(question)
            db.session.commit()
            print(f"{title} 发布成功")
            return redirect(url_for('qa.index'))
        else:
            # 若发布失败，则跳转到发布页面重新发布
            print("发布失败，验证错误详情:", form.errors)
            return redirect(url_for("qa.public_question"))


@qa_bp.route('/detail/<qa_id>', methods=['GET', 'POST'])
def detail(qa_id):
    question = QuestionModel.query.get(qa_id)
    return render_template("detail.html", question=question)


@qa_bp.route('/answer/public', methods=['POST'])
# @qa_bp.post('/answer/public')
@login_required
def public_answer():
    form = AnswerForm(request.form)
    if form.validate():
        content = form.content.data
        question_id = form.question_id.data
        answer = AnswerModel(content=content, question_id=question_id, author = g.user)
        db.session.add(answer)
        db.session.commit()
        print("评论发布成功！")
        return redirect(url_for('qa.detail', qa_id=question_id))
    else:
        print("表单验证失败：", form.errors)
        return redirect(url_for("qa.detail", qa_id=request.form["question_id"]))


@qa_bp.route('/search', methods=['GET'])
def search():
    param = request.args.get('param')
    questions = QuestionModel.query.filter(QuestionModel.title.contains(param)).all()
    return render_template("index.html", questions=questions)


