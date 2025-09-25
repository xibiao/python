from django.shortcuts import render, redirect
from django.db import transaction
from app01.models import Department


def depart_list(request):
    departments = Department.objects.all()
    return render(request, "depart_list.html", {"departs": departments})


# 使用装饰器方式，这种方式需要在settings.py文件的数据库连接信息中添加：'ATOMIC_REQUESTS': True
# @transaction.atomic
def depart_add(request):
    try:
        with transaction.atomic():  # 开启事务块
            if request.method == "GET":
                return render(request, "depart_add.html")
            data = request.POST
            depart_name = data["depart"]
            Department.objects.create(title=depart_name)
            print("新建部门成功")
            return redirect("/depart/list")
    except Exception as e:
        print("新建部门失败：", e)  # 操作数据表异常时Django事务会自动回滚，若是重定向或者其他异常不会回滚
        return render(request, "depart_add.html")


def depart_delete(request):
    # http://127.0.0.1:8000/depart/delete?id=1
    id = request.GET.get("id")
    # 根据id删除数据
    Department.objects.filter(id=id).delete()
    print("成功删除部门：", id)
    return redirect("/depart/list")


def depart_edit(request, id):
    try:
        if request.method == "GET":
            department = Department.objects.get(id=id)
            return render(request, "depart_edit.html", {"depart": department})
        data = request.POST
        depart_name = data["depart"]
        Department.objects.filter(id=id).update(title=depart_name)
        print(f"成功修改部门：{id}，修改后的部门名称是：{depart_name}")
        return redirect("/depart/list")
    except Exception as e:
        print("修改部门失败：", e)
        return render(request, "depart_edit.html", {"err_msg": "修改失败"})
