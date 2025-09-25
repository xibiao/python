from django import forms

from app01.models import UserInfo


class UserForm(forms.ModelForm):
    # ModelForm默认只对字段是否为空进行校验，若要校验其他逻辑，需要自己手动校验
    # 例如，可以对用户名的长度进行校验
    username = forms.CharField(min_length=3, max_length=10, label="用户名")
    # 让密码输入框变成掩码形式（显示为圆点...）
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = UserInfo
        # 由于在UserInfo类中将'create_time'字段设置成了auto_now_add=True，
        # Django默认将auto_now_add或auto_now的DateTimeField自动设为editable=False，
        # 而在Django的ModelForm中不能编辑一个被标记为editable=False的字段，否则报下面的错误
        # django.core.exceptions.FieldError: 'create_time' cannot be specified for UserInfo model form as it is a non-editable field
        # fields = ['username', 'password', 'age', 'gender', 'account', 'depart']
        fields = ['username', 'password', 'age', 'gender', 'account', 'create_time' , 'depart']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if name == 'password':
                field.widget.attrs = {'type': 'password', 'class': 'form-control', 'placeholder': field.label}
            else:
                field.widget.attrs = {'class': 'form-control', 'placeholder': field.label}
