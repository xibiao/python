"""
URL configuration for python_django project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from app01.views import views, user, departs, pretty_nums, user_test, admin, order

# Unresolved reference 'app01'








urlpatterns = [
    # path('admin/', admin.site.urls),
    path('index/', views.index),
    path('login/', views.login),
    path('logout/', views.logout),
    path('user_test/add/', user_test.add),
    path('user_test/query/', user_test.query),
    path('user_test/info/', user_test.get_user_info),
    path('user_test/delete/', user_test.delete),

    # 部门管理
    path('depart/list/', departs.depart_list),
    path('depart/add/', departs.depart_add),
    path('depart/delete/', departs.depart_delete),
    path('depart/<int:id>/edit/', departs.depart_edit),

    # 用户管理
    path('user/list/', user.user_list),
    path('user/add/', user.user_add),
    path('user/<int:id>/edit/', user.user_edit),
    path('user/delete/', user.user_delete),

    # 靓号管理
    path('pretty_num/list/', pretty_nums.pretty_num_list),
    path('pretty_num/add/', pretty_nums.pretty_num_add),
    path('pretty_num/<int:id>/edit/', pretty_nums.pretty_num_edit),
    path('pretty_num/delete/', pretty_nums.pretty_num_delete),
    path('pretty_num/search/', pretty_nums.pretty_num_search),

    # 管理员管理
    path('admin/list/', admin.admin_list),
    path('admin/add/', admin.admin_add),
    path('admin/<int:id>/edit/', admin.admin_edit),
    path('admin/<int:id>/delete/', admin.admin_delete),
    # 生成图片验证码
    path('image/code/', views.gene_image_code),

    # 订单管理
    path('order/list/', order.order_list),
    path('order/add/', order.order_add),
    path('order/delete/', order.order_delete),
    path('order/detail/', order.order_detail),
    path('order/edit/', order.order_edit),

]
