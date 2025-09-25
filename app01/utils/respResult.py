from django.http import JsonResponse
from django.core import serializers
from django.db.models import QuerySet, Model
import json
from typing import Union, Any, Optional


class RespResult:
    """
    Django统一响应封装工具

    功能特性：
    1. 支持多种数据类型自动处理
    2. 标准化的成功/错误响应格式
    3. 完善的类型检查和异常处理
    """

    @staticmethod
    def ok(
            data: Optional[Union[QuerySet, Model, list, dict]] = None,
            msg: str = "success",
            **kwargs
    ) -> JsonResponse:
        """成功响应封装
        Args:
            data: 支持QuerySet/Model实例/字典/列表等类型
            msg: 自定义成功消息
            kwargs: 额外响应字段
        Returns:
            标准格式的JsonResponse
        """
        try:
            processed_data = None
            if data is not None:
                if isinstance(data, (QuerySet, Model)):
                    serialized = serializers.serialize('python', data)
                    processed_data = [item['fields'] for item in serialized]
                elif isinstance(data, list) and data and isinstance(data[0], Model):
                    serialized = serializers.serialize('python', data)
                    processed_data = [item['fields'] for item in serialized]
                else:
                    processed_data = data

            response = {
                "code": 200,
                "msg": msg,
                "data": processed_data,
                **kwargs
            }

            return JsonResponse(
                response,
                json_dumps_params={
                    'ensure_ascii': False,
                    'indent': 2
                }
            )

        except Exception as e:
            return RespResult.error(f"数据处理异常: {str(e)}")


    @staticmethod
    def error(
            msg: str = "internal error",
            code: int = 500,
            data: Any = None,
            **kwargs
    ) -> JsonResponse:
        """错误响应封装
        Args:
            msg: 错误描述信息
            code: 自定义错误码
            data: 错误相关数据
            kwargs: 额外响应字段
        Returns:
            标准错误格式的JsonResponse
        """
        response = {
            "code": code,
            "msg": msg,
            "data": data,
            **kwargs
        }

        return JsonResponse(
            response,
            status=code,
            json_dumps_params={
                'ensure_ascii': False,
                'indent': 2
            }
        )


def response_result(data: Any) -> JsonResponse:
    """统一响应处理器
    Args:
        data: 要处理的数据
    Returns:
        封装后的响应对象
    """
    try:
        if data is None:
            return RespResult.ok()
        if isinstance(data, (QuerySet, Model, list, dict)):
            return RespResult.ok(data)
        return RespResult.error("不支持的参数类型", code=400)
    except Exception as e:
        return RespResult.error(f"处理异常: {str(e)}")
