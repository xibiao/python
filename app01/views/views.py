from django.shortcuts import HttpResponse, render, redirect


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
        return render(request, "index.html")
    data = request.POST
    name = data["username"]
    pwd = data["pwd"]
    if name == "root" and pwd == "123":
        return redirect("http://www.baidu.com/")
    else:
        errorInfo = "用户名或密码错误"
        return render(request, "index.html", {"err_msg": errorInfo})
