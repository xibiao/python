from functools import wraps
from flask import redirect, url_for, g


# 自定义装饰器，若用户还未登录，则先登录，否则直接执行对应操作
def login_required(func):
    # 保留func的信息
    @wraps(func)
    def wrapper(*args, **kwargs):
        if g.user:
            return func(*args, **kwargs)
        else:
            return redirect(url_for("auth.login"))
    return wrapper
