from django.core import serializers

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

from app01.models import UserInfo
from app01.utils.respResult import response_result, RespResult


def insert(request):
    try:
        UserInfo.objects.create(username="lily", password="123", age=20)
        UserInfo.objects.create(username="john", password="456", age=10)
        return HttpResponse("操作成功")
    except Exception as e:
        print("错误信息：", e)
        return HttpResponse("操作失败")


def query(request):
    try:
        # 根据id查询单条数据
        # return queryById(request)
        # 查询全部数据
        return queryAll(request)
    except Exception as e:
        print("异常信息：", e)
        return RespResult.error(str(e))

def queryById(request):
    try:
        user = UserInfo.objects.filter(id=1)
        # result = serializers.serialize("json", user)
        print("查询结果：", serializers.serialize("python", user))
        return response_result(user)
    except Exception as e:
        print("异常信息：", e)
        return RespResult.error(str(e))

def queryAll(request):
    try:
        userAll = UserInfo.objects.all()
        print("查询结果：", serializers.serialize("json", userAll))
        """
        查询结果： [{'model': 'app01.userinfo', 'pk': 1, 'fields': {'username': 'andy', 'password': '123', 'age': 20}}, 
        {'model': 'app01.userinfo', 'pk': 2, 'fields': {'username': 'lily', 'password': '123', 'age': 20}}, 
        {'model': 'app01.userinfo', 'pk': 3, 'fields': {'username': 'john', 'password': '456', 'age': 10}}]
        """
        return response_result(userAll)
    except Exception as e:
        print("异常信息：", e)
        return RespResult.error(str(e))


def update(request):
    UserInfo.objects.filter(username="lily").update(age=20)
    user = UserInfo.objects.filter(id=1).update(age=30)
    return response_result(user)


def deleteByName(request):
    UserInfo.objects.filter(username="lily").delete()
    return RespResult.ok()


def add(request):
    try:
        if request.method == "GET":
            return render(request, "user_test.html")
        data = request.POST
        user = data.get('user')
        pwd = data.get('pwd')
        age = data.get('age')
        print("username:", user + ", password:", pwd)
        UserInfo.objects.create(username=user, password=pwd, age=age)
        return redirect('/user_test/info')
    except Exception as e:
        return RespResult.error(str(e))


def get_user_info(request):
    userAll = UserInfo.objects.all()
    print("查询结果：", serializers.serialize("python", userAll))
    return render(request, "user_test.html", {"data_list": userAll})


def delete(request):
    try:
        id = request.GET.get("id")
        UserInfo.objects.filter(id=id).delete()
        return redirect('/user_test/info')
    except Exception as e:
        return RespResult.error(str(e))


