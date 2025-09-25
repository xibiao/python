from django.db import models

"""
执行以下两条命令，Django会自动创建 app01_userinfo 数据表，
其中app01是项目名称，userinfo是在models.py文件中定义的类名的小写字母
python manage.py makemigrations
python manage.py migrate
"""
class UserInfo(models.Model):
    # null=False表示数据库该字段不允许为空，blank=False表示向表中插入数据提交表单时该字段不能为空
    username = models.CharField(max_length=20, null=False, blank=False)
    password = models.CharField(max_length=20, null=False, blank=False)
    # IntegerField、DateTimeField‌：默认null=True但blank=False，允许数据库存储空值（NULL），但表单提交时必须提供值
    age = models.IntegerField()
    # 若向已存在的表中新增字段，需要设置默认值或者允许为空
    # sex = models.CharField(max_length=4, default='male')
    # sex = models.CharField(max_length=4, null=True, blank=True)





