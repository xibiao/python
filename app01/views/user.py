from django.shortcuts import render, redirect
from app01.models import UserInfo
from app01.forms.model_forms import UserForm


def user_list(request):
    users = UserInfo.objects.all()
    for user in users:
        # print(user.id, user.username, user.create_time.strftime("%Y-%m-%d %H:%M:%S"))
        print(user.id, user.username, user.create_time.strftime("%Y-%m-%d"), user.get_gender_display(),
              user.depart.title)
    return render(request, "user_list.html", {"users": users})


"""
# 原始方式
def user_add(request):
    try:
        if request.method == "GET":
            user = {'gender_choice': UserInfo.gender_choice, 'departs': Department.objects.all()}
            print("新增用户：", user)
            return render(request, "user_add.html", user)
        data = request.POST
        username = data.get('user')
        password = data.get('pwd')
        age = data.get('age')
        gender = data.get('gender')
        account = data.get('account')
        create_time = data.get('ctime')
        depart = data.get('depart')

        UserInfo.objects.create(username=username, password=password, age=age, gender=gender, depart_id=depart,
                                account=account, create_time=create_time)
        print("新增用户成功:", username)
        return redirect("/user/list")
    except Exception as e:
        print(e)
        return render(request, "user_add.html", {"err_msg": "新增用户失败"})
"""


# ModelForm方式
def user_add(request):
    try:
        if request.method == "GET":
            user_form = UserForm()
            print("新增用户：", user_form)
            return render(request, "user_add.html", {"form": user_form})
        # 获取POST方式提交的数据，校验之后若无问题则保存到数据库中
        user_form = UserForm(data=request.POST)
        if user_form.is_valid():
            user_form.save()
            print("新增用户成功:", user_form)
            return redirect("/user/list")
        return render(request, "user_add.html", {"err_msg": "存在非法字段", "form": user_form})
    except Exception as e:
        print("新增用户失败:", e)
        return render(request, "user_add.html", {"err_msg": "新增用户失败"})


def user_edit(request, id):
    try:
        # 从数据库中根据id查询数据
        user_info = UserInfo.objects.get(id=id)
        if request.method == "GET":
            # 将查询到的数据封装到ModelForm中，用于在界面上展示修改之前的数据
            user_form = UserForm(instance=user_info)
            return render(request, 'user_edit.html', {"form": user_form})
        # 获取POST方式提交的数据，校验之后若无问题则保存到数据库中，修改数据时需要提供instance，否则就是新增
        user_form = UserForm(data=request.POST, instance=user_info)
        for field in user_form.fields:
            print(f"post方式-field:{field},value:{getattr(user_info, field)}")
        if user_form.is_valid():
            user_form.save()
            print("修改用户成功:", user_form)
            return redirect("/user/list")
        return render(request, 'user_edit.html', {"err_msg": "存在非法字段", "form": user_form})
    except Exception as e:
        print("修改用户失败:", e)
        return render(request, "user_edit.html", {"err_msg": "修改用户失败"})


"""
注意 user_edit 方法和 user_delete 方法的区别，user_edit方法的路径是/user/{id}/edit/，
user_delete方法的路径是/user/delete，在user_list.html界面点击删除按钮时请求路径是/user/delete?id={id}，
对于/user/{id}/edit/这种请求路径，需要在方法上添加id接收参数值，
而对于/user/delete?id={id}这种请求路径，不要在方法上添加id参数，而是在方法中通过request.GET.get("id")获取参数值
"""
def user_delete(request):
    # 从请求参数中获取"id"，http://127.0.0.1:8000/user/delete/?id=6
    id = request.GET.get("id")
    # 根据id从表中删除数据
    UserInfo.objects.get(id=id).delete()
    # UserInfo.objects.filter(id=id).delete()
    return redirect("/user/list")