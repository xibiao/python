from django import forms
from django.core.validators import RegexValidator, ValidationError
from app01.forms.bootstrap_forms import BootstrapModelForm
from app01.models import UserInfo, PrettyNum, AdminInfo, OrderInfo
from app01.utils.encrypt import md5


class UserForm(BootstrapModelForm):
    # ModelForm默认只对字段是否为空或字段值是否符合表结构设计进行校验，若要校验其他逻辑，需要自己手动校验
    # 例如，可以对用户名的长度进行校验
    username = forms.CharField(min_length=2, max_length=10, label="用户名")
    # 让密码输入框变成掩码形式（显示为圆点...），render_value=True 表示将原密码显示在输入框中
    password = forms.CharField(widget=forms.PasswordInput(render_value=True), min_length=6, label="密码")

    class Meta:
        model = UserInfo
        # 由于在UserInfo类中将'create_time'字段设置成了auto_now_add=True，
        # Django默认将auto_now_add或auto_now的DateTimeField自动设为editable=False，
        # 而在Django的ModelForm中不能编辑一个被标记为editable=False的字段，否则报下面的错误
        # django.core.exceptions.FieldError: 'create_time' cannot be specified for UserInfo model form as it is a non-editable field
        # fields = ['username', 'password', 'age', 'gender', 'account', 'depart']
        fields = ['username', 'password', 'age', 'gender', 'account', 'create_time', 'depart']

    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if name == 'password':
                field.widget.attrs['type'] = 'password'
    """


class PrettyNumModelForm(BootstrapModelForm):
    # 校验方式1
    # 对手机号进行正则校验
    mobile = forms.CharField(label="手机号", validators=[RegexValidator(r'^1[3-9]\d{9}$', '手机号格式错误')])

    class Meta:
        model = PrettyNum
        # fields = "__all__"
        # exclude = ['level']
        fields = ['mobile', 'price', 'level', 'status']

    """
    # 校验方式2：钩子函数，函数名是"clean_字段名"
    def clean_mobile(self):
        # 获取用户输入的"mobile"字段的值
        mobile = self.cleaned_data['mobile']
        pattern = re.compile(r'^1[3-9]\d{9}$')
        if pattern.match(mobile) is None:
            raise ValidationError('手机号格式错误')
        numFromDb = PrettyNum.objects.filter(mobile=mobile).first()
        # is_exists = PrettyNum.objects.filter(mobile=mobile).exists()
        if numFromDb:
            raise ValidationError('该手机号已存在，请更换一个手机号')
        # 若验证通过，则返回用户输入的数据
        return mobile
    """


class PrettyNumEditModelForm(BootstrapModelForm):
    # 显示"手机号"但是不可修改
    # mobile = forms.CharField(label="手机号", disabled=True,
    #                          validators=[RegexValidator(r'^1[3-9]\d{9}$', '手机号格式错误')])
    # 校验方式1：对手机号进行正则校验
    mobile = forms.CharField(label="手机号", validators=[RegexValidator(r'^1[3-9]\d{9}$', '手机号格式错误')])

    class Meta:
        model = PrettyNum
        # exclude = ['mobile']
        fields = ['mobile', 'price', 'level', 'status']

    # 校验方式2：钩子函数，函数名是"clean_字段名"
    def clean_mobile(self):
        # 获取用户输入的"mobile"字段的值
        mobile = self.cleaned_data['mobile']
        # 获取当前修改数据记录的主键id
        pk = self.instance.pk
        # numFromDb = PrettyNum.objects.filter(mobile=mobile).exclude(id=pk).first()
        # 判断 mobile = 'xxx' 且 id != pk 的数据是否存在
        is_exists = PrettyNum.objects.filter(mobile=mobile).exclude(id=pk).exists()
        if is_exists:
            raise ValidationError('该手机号已存在，请更换一个手机号')
        # 若验证通过，则返回用户输入的数据，该数据需要保存到数据库中
        return mobile


class AdminModelForm(BootstrapModelForm):
    # ModelForm默认只对字段是否为空或字段值是否符合表结构设计进行校验，若要校验其他逻辑，需要自己手动校验
    # 例如，可以对用户名的长度进行校验
    username = forms.CharField(min_length=2, max_length=10, label="用户名")
    # 让密码输入框变成掩码形式（显示为圆点...），render_value=True 表示将原密码显示在输入框中
    password = forms.CharField(widget=forms.PasswordInput(render_value=True), min_length=6, label="密码")
    confirm_password = forms.CharField(widget=forms.PasswordInput(render_value=True), label="确认密码")

    class Meta:
        model = AdminInfo
        fields = ['username', 'password']

    # 钩子函数，对 password 字段进行加密，保存到数据库的是加密后的密码
    def clean_password(self):
        password = self.cleaned_data['password']
        return md5(password)

    # 钩子函数，对 confirm_password 字段进行校验
    def clean_confirm_password(self):
        password = self.cleaned_data['password']
        confirm_password = md5(self.cleaned_data['confirm_password'])
        if password != confirm_password:
            raise ValidationError("确认密码必须与密码保持一致")
        return confirm_password


class LoginForm(forms.Form):
    username = forms.CharField(label="用户名", widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="密码",
                               widget=forms.PasswordInput(render_value=True, attrs={'class': 'form-control'}))
    code = forms.CharField(label="验证码", widget=forms.TextInput(attrs={'class': 'form-control'}))


class OrderModelForm(BootstrapModelForm):
    class Meta:
        model = OrderInfo
        # fields = "__all__"
        # 在界面上不展示'order_no', 'user'(外键对应的表字段是user_id)
        exclude = ['order_no', 'user']

