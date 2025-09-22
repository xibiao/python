import random
import string

from flask import Blueprint, render_template, jsonify, request, redirect, url_for, session
from flask_mail import Message
from app import mail
import models
from blueprints.forms import RegisterForm, LoginForm
from exts import db
from models import UserModel
from werkzeug.security import generate_password_hash, check_password_hash

# 创建蓝图
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


# 在浏览器上访问http://127.0.0.1:5000/auth/register，此时是GET请求，给浏览器返回一个注册页面register.html，
# 在register.html文件中使用了static/js/register.js文件，在register.js中会调用/auth/email/captcha接口给邮箱发送验证码，
# 在浏览器上填写好邮箱、验证码、用户名、密码等表单信息之后，点击"立即注册"按钮，此时是POST请求，将填写的表单信息保存到数据表中
@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        # 验证邮箱与验证码是否匹配且正确
        # 表单验证需要使用flask-wtf(对wtforms的封装)，pip install flask-wtf
        form = RegisterForm(request.form)
        print(f"email={form.email.data}, password={form.password.data}, valid={form.validate()}")
        if form.validate():
            email = form.email.data
            password = form.password.data
            username = form.username.data
            # 给密码进行加密
            user = models.UserModel(username=username, email=email, password=generate_password_hash(password))
            db.session.add(user)
            db.session.commit()
            print("注册成功，进入到登录页面")
            # 若注册成功，则跳转到登录页面
            return redirect(url_for("auth.login"))
        else:
            # 若注册失败，则跳转到注册页面重新注册
            print("注册失败，请重新注册。验证错误详情:", form.errors)
            return redirect(url_for("auth.register"))


# 通过邮箱获取验证码，在static/js/register.js文件中会调用该接口给邮箱发送验证码
# 在浏览器或postman发起GET请求：http://127.0.0.1:5000/auth/email/captcha?email=xxx@qq.com
@auth_bp.route('/email/captcha')
def get_email_captcha():
    try:
        email = request.args.get('email')
        source = string.digits * 4
        # 从source中随机获取6个字符组成一个列表，如['4', '0', '8', '3', '5', '3']
        chars = random.sample(source, 6)
        captcha = "".join(chars)
        message = Message(subject="注册验证码", recipients=[email], body=f"您的验证码是{captcha}，请妥善保管！")
        mail.send(message)
        email_captcha = models.EmailCaptchaModel(email=email, captcha=captcha)
        db.session.add(email_captcha)
        db.session.commit()
        # return f"成功发送验证码：{captcha} 到邮箱：{email}"
        # return jsonify(model_to_dict(email_captcha))
        # 注意：此处需要返回json字符串，其返回值必须有'code'字段，
        # 因为在register.js中调用该接口得到响应结果，从响应结果获取'code'字段
        return jsonify({'code': 200, 'message': '验证码已发送'}), 200
    except Exception as e:
        return jsonify({'code': 500, "error": str(e)}), 500


# @auth_bp.route('/email')
# def send_email():
#     try:
#         message = Message("邮箱测试", ["1814482143@qq.com"], "这是一条测试邮件，无需回复")
#         mail.send(message)
#         return "邮件发送成功！"
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        form = LoginForm(request.form)
        if form.validate():
            email = form.email.data
            # 用户提交表单中的密码是明文密码，数据库中存储的是密文密码
            password = form.password.data
            user = UserModel.query.filter_by(email=email).first()
            # 若用户不存在，说明该邮箱还未被注册
            if not user:
                print("该邮箱还未被注册，请先注册再登录！或者使用正确的邮箱登录！")
                return redirect(url_for('auth.login'))
            if check_password_hash(user.password, password):
                session['user_id'] = user.id
                # 重定向到首页
                # return redirect('/')
                return redirect(url_for('qa.index'))
            else:
                print("密码错误，请重新登陆！")
                return redirect(url_for('auth.login'))
        else:
            # 邮箱或密码错误，重新登陆
            print("邮箱或密码错误，请重新登陆！")
            return redirect(url_for("auth.login"))


@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))


