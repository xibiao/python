from django.shortcuts import render, redirect
from app01.models import PrettyNum
from app01.forms.model_forms import PrettyNumModelForm, PrettyNumEditModelForm
from app01.utils.pageUtil import Pagination


def pretty_num_list(request):
    """
    for i in range(100):
        # 随机生成一个8位数的整数
        random_number = random.randint(10000000, 99999999)
        num = "130" + str(random_number)
        PrettyNum.objects.create(mobile=num, price=100, level=1, status=2)
    """
    # select * from app01_prettynum order by level desc;
    condition = {}
    param = request.GET.get("search")
    if param:
        # 如果param不为空，则作为条件进行过滤，否则表示查询全部
        print("param======", param)
        condition = {"mobile__contains": param}
    else:
        param = "130"
    queryset = PrettyNum.objects.filter(**condition).order_by("-level")
    # queryset = PrettyNum.objects.filter(mobile__contains=param).order_by("-level")

    page_obj = Pagination(request, queryset)
    page_queryset = page_obj.page_queryset
    page_str = page_obj.generate_page_html()
    '''
    start = (cur_page - 1) * page_size
    end = start + page_size
    page_queryset = PrettyNum.objects.filter(**condition).order_by("-level")[start:end]

    # 获取数据总条数
    total_count = PrettyNum.objects.filter(**condition).order_by("-level").count()
    # total_page_count 和 div 分别表示 total_count 除以 page_size 的商和余数
    total_page_count, div = divmod(total_count, page_size)
    # 若余数不为0，则总页数 total_page_count 需要加一
    if div:
        total_page_count += 1
    print(f"total_count={total_count}, total_page_count={total_page_count}", total_count, total_page_count)
    
    # 间隔space表示在当前页码前后分别间隔的页数，假设当前页码是5，space=3，则界面展示的页数是[2,3,4,5,6,7,8]
    space = 5
    # 在前端界面默认只展示(2 * space + 1)页，如果总页数小于等于(2 * space + 1)，无需让页码滚动
    if total_page_count <= 2 * space + 1:
        start_page = 1
        end_page = total_page_count
    else:
        # 若当前页码小于等于间隔space，为了防止页码向前翻滚变成0或负数，则让 start_page = 1
        if cur_page <= space:
            start_page = 1
            end_page = 2 * space + 1
        # 为了防止无限向后翻滚页码，若当前页码大于 total_page_count - space，则停止页码向后翻滚
        elif cur_page > total_page_count - space:
            start_page = total_page_count - 2 * space
            end_page = total_page_count
        # 若当前页码向前翻滚不会变成0或负数，且向后翻滚不会超过最大页码，则让当前页码可以向前或向后翻滚
        else:
            start_page = cur_page - space
            end_page = cur_page + space

    page_str_list = []
    first_page = '<li><a href="?page={}">首页</a></li>'.format(1)
    page_str_list.append(first_page)
    if cur_page > 1:
        prev_page = '<li><a href="?page={}">上一页</a></li>'.format(cur_page - 1)
    else:
        prev_page = '<li><a href="?page={}">上一页</a></li>'.format(1)
    page_str_list.append(prev_page)

    # range函数是左闭右开的，即取前不取后
    for i in range(start_page, end_page + 1):
        # 若是当前页，则添加class="active"属性，标记是当前选择的页码
        if i == cur_page:
            ele = '<li class="active"><a href="?page={}">{}</a></li>'.format(i, i)
        else:
            ele = '<li><a href="?page={}">{}</a></li>'.format(i, i)
        page_str_list.append(ele)

    if cur_page < total_page_count:
        next_page = '<li><a href="?page={}">下一页</a></li>'.format(cur_page + 1)
    else:
        next_page = '<li><a href="?page={}">下一页</a></li>'.format(total_page_count)
    page_str_list.append(next_page)
    last_page = '<li><a href="?page={}">尾页</a></li>'.format(total_page_count)
    page_str_list.append(last_page)

    skip_page = """
    <li>
    	<form method="get" style="float: left; margin-left: 2px">
    		<input type="text" name="page" class="form-control" placeholder="页码"
    		style="position: relative;float: left;display: inline-block;width: 80px;border-radius: 0">
    		<button class="btn btn-default" type="submit" style="border-radius: 0">跳转</button>
    	</form>
    </li>
    """
    page_str_list.append(skip_page)

    page_str = mark_safe("".join(page_str_list))
    '''
    # param是用户输入的检索数据，将用户输入的数据回显到前端界面上
    context = {"search_data": param, "pretty_nums": page_queryset, "page_str": page_str}
    return render(request, "pretty_num_list.html", context)


def pretty_num_add(request):
    try:
        if request.method == "GET":
            form = PrettyNumModelForm()
            return render(request, "pretty_num_add.html", {"form": form})
        data = request.POST
        form = PrettyNumModelForm(data=data)
        if form.is_valid():
            form.save()
            print("新增靓号成功：", form)
            return redirect("/pretty_num/list")
        return render(request, "pretty_num_add.html", {"form": form, "err_msg": "存在非法字段"})
    except Exception as e:
        print("新增靓号失败：", e)
        return render(request, "pretty_num_add.html", {"err_msg": "新增靓号失败"})


def pretty_num_edit(request, id):
    try:
        num = PrettyNum.objects.get(id=id)
        if not num:
            # return render(request, "pretty_num_edit.html", {"err_msg": f"靓号{id}不存在"})
            raise RuntimeError(f"靓号{id}不存在")
        if request.method == "GET":
            # 将查询到的数据封装到ModelForm中，用于在界面上展示修改之前的数据
            form = PrettyNumEditModelForm(instance=num)
            return render(request, "pretty_num_edit.html", {"form": form})
        data = request.POST
        form = PrettyNumEditModelForm(data=data, instance=num)
        if form.is_valid():
            form.save()
            print("修改靓号成功：", form)
            return redirect("/pretty_num/list")
        return render(request, "pretty_num_edit.html", {"form": form, "err_msg": "存在非法字段"})
    except Exception as e:
        print("修改靓号失败：", e)
        return render(request, "pretty_num_edit.html", {"err_msg": "修改靓号失败"})


def pretty_num_delete(request):
    id = request.GET.get("id")
    data_from_db = PrettyNum.objects.get(id=id)
    if not data_from_db:
        return render(request, "pretty_num_list.html", {"err_msg": f"靓号{id}不存在"})
    PrettyNum.objects.get(id=id).delete()
    return redirect("/pretty_num/list")


def pretty_num_search(request):
    # num1 = PrettyNum.objects.filter(mobile="15888888888", id=5).first()
    # num2 = PrettyNum.objects.filter(mobile=request.GET.get("mobile"), id=request.GET.get("id")).first()
    # condition = {'mobile': request.GET.get("mobile"), 'id': request.GET.get("id")}
    # condition = {"mobile__contains": "888", "level__gt": 3}
    # nums = PrettyNum.objects.filter(**condition)
    # num4 = PrettyNum.objects.filter(**{}).order_by("-level")  # 空字典表示查询全部
    # num5 = PrettyNum.objects.all().order_by("-level")
    # num6 = PrettyNum.objects.filter(mobile__startswith="131")  # 查询所有以"131"开头的手机号
    # num7 = PrettyNum.objects.filter(level__gt=3)  # 查询level>3的所有数据
    # __icontains 表示不区分大小写的模糊查询，__contains 表示区分大小写的模糊查询
    # contain_nums = PrettyNum.objects.filter(mobile__icontains=request.GET.get("mobile")).order_by("-level")
    # param是接收用户输入的数据
    param = request.GET.get("search")
    print("param======", param)
    # 如果param为空，则表示查询全部，相当于/pretty_num/list接口，可以将/search/与/list/这两个接口合并
    condition = {"mobile__contains": param}
    nums = PrettyNum.objects.filter(**condition).order_by("-level")
    # nums = PrettyNum.objects.filter(mobile__contains=param).order_by("-level")
    return render(request, "pretty_num_list.html", {"pretty_nums": nums, "param": param})
