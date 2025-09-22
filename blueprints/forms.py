import wtforms
from wtforms.validators import Email, Length, EqualTo, InputRequired

from models import UserModel
from models import EmailCaptchaModel
from exts import db


# 验证前端提交的数据是否符合要求
class RegisterForm(wtforms.Form):
    # pip install email_validator
    email = wtforms.StringField(validators=[Email("邮箱格式错误！")])
    captcha = wtforms.StringField(validators=[Length(min=6, max=6, message="验证码格式错误！")])
    username = wtforms.StringField(validators=[Length(min=3, max=20, message="用户名长度不符合要求！")])
    password = wtforms.StringField(validators=[Length(min=6, max=20, message="密码长度不符合要求！")])
    password_confirm = wtforms.StringField(validators=[EqualTo("password", message="两次密码不一致！")])


    # 自定义验证逻辑
    # 验证邮箱是否被注册
    def validate_email(self, field):
        email = field.data
        user = UserModel.query.filter_by(email=email).first()
        if user:
            raise wtforms.ValidationError(message="该邮箱已被注册！")

    # 验证码是否与邮箱匹配，验证码是否正确
    def validate_captcha(self, field):
        captcha = field.data
        email = self.email.data
        email_captcha = EmailCaptchaModel.query.filter_by(email=email, captcha=captcha).first()
        if not email_captcha:
            raise wtforms.ValidationError(message="邮箱或验证码错误！")
        # else:
        # # 可以在表中新增一个字段用于标记验证码是否已使用，使用脚本定期删除已使用的验证码
        #     db.session.delete(email_captcha)
        #     db.session.commit()


class LoginForm(wtforms.Form):
    email = wtforms.StringField(validators=[Email("邮箱格式错误！")])
    password = wtforms.StringField(validators=[Length(min=6, max=20, message="密码长度不符合要求！")])


class QuestionForm(wtforms.Form):
    title = wtforms.StringField(validators=[Length(min=3, max=100, message="标题格式错误！")])
    content = wtforms.StringField(validators=[Length(min=3, message="内容格式错误！")])


class AnswerForm(wtforms.Form):
    content = wtforms.StringField(validators=[Length(min=3, message="内容格式错误！")])
    question_id = wtforms.IntegerField(validators=[InputRequired(message="必须传入问题id")])

