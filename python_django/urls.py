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

from django.contrib import admin
from django.urls import path
from app01 import views, user_test, departs, user
# Unresolved reference 'app01'








urlpatterns = [
    # path('admin/', admin.site.urls),
    path('index/', views.index),
    path('login/', views.login),
    path('user_test/add/', user_test.add),
    path('user_test/query/', user_test.query),
    path('user_test/info/', user_test.get_user_info),
    path('user_test/delete/', user_test.delete),

    path('depart/list/', departs.depart_list),
    path('depart/add/', departs.depart_add),
    path('depart/delete/', departs.depart_delete),
    path('depart/<int:id>/edit/', departs.depart_edit),

    path('user/list/', user.user_list),
    path('user/add/', user.user_add),
    path('user/<int:id>/edit/', user.user_edit),
    path('user/delete/', user.user_delete),

]
