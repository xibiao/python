# 创建Django项目的步骤：
# 1、首先安装Django：pip install django
# 2、在终端通过 "python manage.py startapp app01" 命令创建一个app项目，此处的项目名称是app01
例如 D:\ProgramFiles\workspace\com\learn\python\python-web\python-django> python manage.py startapp app01
创建之后的目录结构如下所示：
D:\ProgramFiles\workspace\com\learn\python\python-web\python-django>tree /F
卷 新加卷 的文件夹 PATH 列表
卷序列号为 12C7-9BDA
D:.
│  manage.py
│
├─.idea
│  │  misc.xml
│  │  modules.xml
│  │  python-django.iml
│  │  vcs.xml
│  │  workspace.xml
│  │
│  └─inspectionProfiles
│          profiles_settings.xml
│
├─app01
│  │  admin.py
│  │  apps.py
│  │  models.py
│  │  tests.py
│  │  views.py
│  │  __init__.py
│  │
│  └─migrations
│          __init__.py
│
└─python_django
    │  asgi.py
    │  settings.py
    │  urls.py
    │  wsgi.py
    │  __init__.py
    │
    └─__pycache__
            settings.cpython-313.pyc
            __init__.cpython-313.pyc

# 3、修改python_django/settings.py文件，注册创建的app项目
# 注意：settings.py文件中有几处需要修改都已标明，按照文件中的要求进行修改
在 INSTALLED_APPS 中添加 'app01.apps.App01Config'，App01Config 是 app01/apps.py文件中的类名，如下所示：
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'app01.apps.App01Config',
]


# 4.在 python_django/urls.py 文件中添加 URL与函数 的映射关系，例如：
from app01 import views
urlpatterns = [
    path('index/', views.index),
]

# 5.在 app01/views.py 文件中创建 index 函数，例如：
from django.shortcuts import HttpResponse, render
def index(request):
    # 或者创建 app01/templates/index.html 文件
    # return render(request, 'index.html')
    return HttpResponse("Hello, world. You're at the polls index.")

# 6.点击运行按钮启动项目，或者在终端执行命令：python manage.py runserver [8000]，默认占用8000端口
在浏览器上访问 http://127.0.0.1:8000/index/ ，验证结果
