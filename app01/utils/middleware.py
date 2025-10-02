from django.http import HttpResponseRedirect
from django.utils.deprecation import MiddlewareMixin


class LoginMiddleware(MiddlewareMixin):
    # 若 process_request 方法有返回值(非None值)，则从当前中间件中断，不再继续向后执行
    def process_request(self, request):
        # 对于不需要拦截的请求路径，则允许放行
        # if request.path.startswith('/login'):
        if request.path_info in ['/login/', '/image/code/']:
            return None
        info = request.session.get('info')
        # print("LoginMiddleware_process_request：", info)
        if not info:
            print("请先登录")
            return HttpResponseRedirect('/login')
        return None

    def process_response(self, request, response):
        # print("LoginMiddleware_process_response：")
        return response

