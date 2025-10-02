from django.shortcuts import render, redirect

from app01.models import AdminInfo
from app01.forms.model_forms import AdminModelForm
from app01.utils.pageUtil import Pagination


def admin_list(request):
    datas = AdminInfo.objects.all()
    page_obj = Pagination(request, datas)
    context = {'queryset': page_obj.page_queryset, 'page_str': page_obj.generate_page_html()}
    return render(request, 'admin_list.html', context)


def admin_add(request):
    try:
        if request.method == "GET":
            form = AdminModelForm()
            return render(request, 'admin_add.html', {'form': form})
        form = AdminModelForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('/admin/list/')
        return render(request, 'admin_add.html', {'form': form, "err_msg": "存在非法字段"})
    except Exception as e:
        print("新增失败：", e)
        return render(request, 'admin_add.html', {"err_msg": "新增失败"})


def admin_edit(request, id):
    try:
        data_from_db = AdminInfo.objects.get(id=id)
        if not data_from_db:
            # return render(request, 'admin_edit.html', {"err_msg": f"管理员{id}不存在"})
            raise RuntimeError(f"管理员{id}不存在")
        if request.method == "GET":
            form = AdminModelForm(instance=data_from_db)
            return render(request, 'admin_edit.html', {'form': form})
        form = AdminModelForm(data=request.POST, instance=data_from_db)
        if form.is_valid():
            form.save()
            return redirect('/admin/list/')
        return render(request, 'admin_edit.html', {'form': form})
    except Exception as e:
        print("修改失败：", e)
        return render(request, 'admin_edit.html', {'err_msg': '修改失败'})


def admin_delete(request, id):
    try:
        data_from_db = AdminInfo.objects.get(id=id)
        if not data_from_db:
            return render(request, 'admin_list.html', {"err_msg": f"管理员{id}不存在"})
        AdminInfo.objects.filter(id=id).delete()
        return redirect('/admin/list/')
    except Exception as e:
        print("删除失败：", e)
        return redirect('/admin/list/')

