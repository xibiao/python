from io import BytesIO
import os

from django.conf import settings
from django.shortcuts import HttpResponse, render, redirect

from app01.forms.model_forms import LoginForm
from app01.models import AdminInfo
from app01.utils.encrypt import md5
from app01.utils.captcha import Captcha


# Create your views here.

def index(request):
    # return HttpResponse("Hello, world. You're at the polls index.")
    master = "andy"
    user_list = [{"username": "John", "password": "123"}, {"username": "Smith", "password": "456"}]
    user_tuple = (("John", "123"), ("Smith", "456"))
    print(user_tuple)
    return render(request, 'index.html',
                  {"login_user": master, "users": user_list, "user_tuples": user_tuple})


def login(request):
    if request.method == "GET":
        form = LoginForm()
        return render(request, "login.html", {"form": form})
    form = LoginForm(data=request.POST)
    if form.is_valid():
        username = form.cleaned_data['username']
        password = md5(form.cleaned_data['password'])
        user_input_code = form.cleaned_data.pop('code')
        code = request.session.get('image_code')
        print("user_input_code:", user_input_code, ", code:", code)
        # 若code为None(验证码已过期)，或者用户输入的验证码与生成的图片验证码不同，则提示"验证码错误或者已过期"
        if (not code) or (user_input_code.upper() != code.upper()):
            # form.add_error("code", "验证码错误或者已过期")
            return render(request, "login.html", {"form": form, "err_msg": "验证码错误或者已过期"})
        # admin_obj = AdminInfo.objects.filter(**form.cleaned_data).first()
        admin_obj = AdminInfo.objects.filter(username=username, password=password).first()
        if not admin_obj:
            # form.add_error("password", "用户名或密码错误")
            return render(request, "login.html", {"form": form, "err_msg": "用户名或密码错误"})
        # 生成随机字符串返回给浏览器存放到cookie中，同时将随机字符串与'info'一同保存到服务器的session中
        # session是个逻辑概念，实际上存储session的地方可以是数据库、Redis等，例如Django将session存储到django_session表中
        request.session['info'] = {'id': admin_obj.id, 'username': admin_obj.username}
        # 登录成功之后从session中删除验证码'image_code'，防止再次被使用，同时设置7天免登录
        request.session.delete('image_code')
        request.session.set_expiry(60 * 60 * 24 * 7)
        return render(request, "basic_layout.html")
    return render(request, "login.html", {"form": form})


def logout(request):
    request.session.clear()
    return redirect("/login/")


def gene_image_code(request):
    # 获取静态文件目录（在settings.py文件中 STATICFILES_DIRS 配置为[BASE_DIR / 'app01']）
    static_dir = settings.STATICFILES_DIRS[0]
    # 获取字体文件的绝对路径
    font_path = os.path.join(static_dir, 'static/font', 'Monaco.ttf')
    # 或使用static函数
    # font_path = os.path.join(settings.BASE_DIR, 'app01/static/font', 'Monaco.ttf')
    # print("font_path===", font_path)
    img, verify_code = Captcha.check_code(font_file=font_path)
    print("生成图片验证码code:", verify_code)
    # 将生成的图片验证码保存到session中(便于与用户输入的验证码进行比对)，并设置180秒超时
    request.session['image_code'] = verify_code
    request.session.set_expiry(180)
    # 将图片验证码写入内存
    stream = BytesIO()
    img.save(stream, 'png')
    return HttpResponse(stream.getvalue(), content_type='image/png')
