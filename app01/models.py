import datetime

from django.db import models

"""
执行以下两条命令，Django会自动创建 app01_userinfo 数据表，
其中app01是项目名称，userinfo是在models.py文件中定义的类名的小写字母
python manage.py makemigrations
python manage.py migrate
"""


class UserInfo(models.Model):
    """用户信息表"""
    # null=False表示数据库该字段不允许为空，blank=False表示向表中插入数据提交表单时该字段不能为空
    username = models.CharField(verbose_name="用户名", max_length=20, null=False, blank=False)
    password = models.CharField(verbose_name="密码", max_length=40, null=False, blank=False)
    # IntegerField、DateTimeField‌：默认null=True但blank=False，允许数据库存储空值（NULL），但表单提交时必须提供值
    age = models.IntegerField(verbose_name="年龄")
    # 若向已存在的表中新增字段，需要设置默认值或者允许为空
    # gender = models.CharField(max_length=4, default='男')
    # gender = models.CharField(max_length=4, null=True, blank=True)
    gender_choice = ((1, '男'), (2, '女'))
    gender = models.SmallIntegerField(verbose_name="性别", choices=gender_choice, default=1)
    account = models.DecimalField(verbose_name="账户余额", max_digits=10, decimal_places=2, default=0)
    # create_time = models.DateTimeField(verbose_name="入职时间", auto_now_add=True, null=True, blank=True)
    create_time = models.DateField(verbose_name="入职时间", default=datetime.datetime.now)
    # 关联外键，此处外键字段名称是"depart"，实际上Django会自动在后面加上_id，即depart_id，to表示需要关联的表，
    # to_field表示通过关联表的哪个字段与本表关联，on_delete表示删除关联表中的数据时如何处理本表的数据
    # models.CASCADE表示删除关联表(此处是部门表)中的数据时，级联删除本表(用户信息表)中对应的数据
    depart = models.ForeignKey(verbose_name="所属部门", to="Department", to_field="id", on_delete=models.CASCADE,
                               null=True, blank=True)
    # models.SET_NULL表示删除关联表(此处是部门表)中的数据时，不删除本表(用户信息表)中的数据，让外键置空（前提是允许外键为空）
    # depart = models.ForeignKey(to="Department", to_field="id", null=True, blank=True, on_delete=models.SET_NULL)


class Department(models.Model):
    """部门表"""
    title = models.CharField(verbose_name="部门名称", max_length=24, null=False, blank=False)

    # print(Department对象)就会调用__str__方法，类似于java中的toString方法
    def __str__(self):
        return self.title


class PrettyNum(models.Model):
    """靓号表"""
    mobile = models.CharField(verbose_name="手机号", max_length=11)
    price = models.IntegerField(verbose_name="价格")
    level_choices = ((1, '1级'), (2, '2级'), (3, '3级'), (4, '4级'))
    level = models.SmallIntegerField(verbose_name="级别", choices=level_choices, default=1)
    status_choices = ((1, '已占用'), (2, '未使用'))
    status = models.SmallIntegerField(verbose_name="状态", choices=status_choices, default=2)



class AdminInfo(models.Model):
    """管理员信息表"""
    # null=False表示数据库该字段不允许为空，blank=False表示向表中插入数据提交表单时该字段不能为空
    username = models.CharField(verbose_name="用户名", max_length=20, null=False, blank=False)
    # md5加密后密码长度是32，例如：4cb71e3e8025a4b1d36801e482170a00
    password = models.CharField(verbose_name="密码", max_length=40, null=False, blank=False)


