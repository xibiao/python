from django.utils.safestring import mark_safe

class Pagination(object):
    """
    自定义的分页组件
    """
    def __init__(self, request, queryset, page_size=10, space = 5):
        """
        :param request: 请求对象
        :param queryset: 复合条件的需要分页的数据
        :param page_size: 每页显示的数据条数
        :param space: 在当前页码前后分别间隔的页数，假设当前页码是5，space=3，则界面展示的页数是[2,3,4,5,6,7,8]
        """
        # 分页，若请求头没有"page"参数，则默认当前页码 cur_page=1
        cur_page = int(request.GET.get("page", "1"))
        if not all(isinstance(x, int) and x > 0 for x in (cur_page, page_size)):
            raise TypeError("当前页码与每页条数必须是大于0的整数。")
        self.cur_page = cur_page
        self.page_size = page_size
        self.start = (cur_page - 1) * page_size
        self.end = cur_page * page_size
        self.page_queryset = queryset[self.start:self.end]
        self.space = space

        # 获取数据总条数
        total_count = queryset.count()
        # total_page_count 和 div 分别表示 total_count 除以 page_size 的商和余数
        total_page_count, div = divmod(total_count, page_size)
        # 若余数不为0，则总页数 total_page_count 需要加一
        if div:
            total_page_count += 1
        self.total_page_count = total_page_count


    def get_start_end_page(self):
        # 间隔space表示在当前页码前后分别间隔的页数，假设当前页码是5，space=3，则界面展示的页数是[2,3,4,5,6,7,8]
        # 在前端界面默认只展示(2 * space + 1)页，如果总页数小于等于(2 * space + 1)，无需让页码滚动
        if self.total_page_count <= 2 * self.space + 1:
            start_page = 1
            end_page = self.total_page_count
        else:
            # 若当前页码小于等于间隔space，为了防止页码向前翻滚变成0或负数，则让 start_page = 1
            if self.cur_page <= self.space:
                start_page = 1
                end_page = 2 * self.space + 1
            # 为了防止无限向后翻滚页码，若当前页码大于 total_page_count - space，则停止页码向后翻滚
            elif self.cur_page > self.total_page_count - self.space:
                start_page = self.total_page_count - 2 * self.space
                end_page = self.total_page_count
            # 若当前页码向前翻滚不会变成0或负数，且向后翻滚不会超过最大页码，则让当前页码可以向前或向后翻滚
            else:
                start_page = self.cur_page - self.space
                end_page = self.cur_page + self.space
        return start_page, end_page


    def generate_page_html(self):
        start_page, end_page = self.get_start_end_page()
        # 定义一个列表，用于存储页码标签，当进行分页查询时，可以动态生成页码
        page_str_list = []
        first_page = '<li><a href="?page={}">首页</a></li>'.format(1)
        page_str_list.append(first_page)
        if self.cur_page > 1:
            prev_page = '<li><a href="?page={}">上一页</a></li>'.format(self.cur_page - 1)
        else:
            prev_page = '<li><a href="?page={}">上一页</a></li>'.format(1)
        page_str_list.append(prev_page)

        # range函数是左闭右开的，即取前不取后
        for i in range(start_page, end_page + 1):
            # 若是当前页，则添加class="active"属性，标记是当前选择的页码
            if i == self.cur_page:
                ele = '<li class="active"><a href="?page={}">{}</a></li>'.format(i, i)
            else:
                ele = '<li><a href="?page={}">{}</a></li>'.format(i, i)
            page_str_list.append(ele)

        if self.cur_page < self.total_page_count:
            next_page = '<li><a href="?page={}">下一页</a></li>'.format(self.cur_page + 1)
        else:
            next_page = '<li><a href="?page={}">下一页</a></li>'.format(self.total_page_count)
        page_str_list.append(next_page)
        last_page = '<li><a href="?page={}">尾页</a></li>'.format(self.total_page_count)
        page_str_list.append(last_page)
        # 跳转到具体某一页码的HTML标签
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

        return mark_safe("".join(page_str_list))