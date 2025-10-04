import json
import random
from datetime import datetime
from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from app01.forms.model_forms import OrderModelForm
from app01.models import OrderInfo
from app01.utils.pageUtil import Pagination


def order_list(request):
    # 根据id倒序排序查询所有订单
    queryset = OrderInfo.objects.all().order_by('-id')
    page_obj = Pagination(request, queryset)
    form = OrderModelForm()
    context = {
        'form': form,
        'queryset': page_obj.page_queryset,
        'page_str': page_obj.generate_page_html()
    }
    return render(request, 'order_list.html', context)


@csrf_exempt
def order_add(request):
    form = OrderModelForm(data=request.POST)
    if form.is_valid():
        # 给order_no字段赋值
        form.instance.order_no = datetime.now().strftime('%Y%m%d%H%M%S') + str(random.randint(10000, 999999))
        # 购买商品的用户不应该让用户手动输入，应该从登录session中获取，session中存放的数据如下所示：
        # request.session['info'] = {'id': admin_obj.id, 'username': admin_obj.username}
        form.instance.user_id = request.session['info']['id']
        # 保存到数据库中
        form.save()
        # return HttpResponse(json.dumps({'status': 'success'}))
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'fail', 'errors': form.errors})


def order_delete(request):
    order_id = request.GET.get('order_id')
    isExist = OrderInfo.objects.filter(id=order_id).exists()
    if not isExist:
        return JsonResponse({'status': 'fail', 'errors': '数据不存在，删除失败！'})
    OrderInfo.objects.filter(id=order_id).delete()
    return JsonResponse({'status': 'success'})


def order_detail(request):
    order_id = request.GET.get('order_id')
    # order = OrderInfo.objects.get(id=order_id)
    # 通过values(*fields)可以得到数据字典，例如：{'goods_name': '手机', 'price': 4000, 'status': 1}
    data_dict = OrderInfo.objects.filter(id=order_id).values('goods_name', 'price', 'status').first()
    print(data_dict)
    if not data_dict:
        return JsonResponse({'status': 'fail', 'errors': '数据不存在'})
    return JsonResponse({'status': 'success', 'data': data_dict})


@csrf_exempt
def order_edit(request):
    order_id = request.GET.get('order_id')
    order = OrderInfo.objects.get(id=order_id)
    if not order:
        return JsonResponse({'status': 'fail', 'err_msg': '数据不存在'})
    form = OrderModelForm(data=request.POST, instance=order)
    if form.is_valid():
        form.save()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'fail', 'errors': form.errors})

