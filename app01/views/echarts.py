from django.http import JsonResponse
from django.shortcuts import render, redirect


def echarts_list(request):
    return render(request, 'echarts_list.html')


def echarts_bar(request):
    # 模拟从数据库查询到的数据
    legend_data = ['销量', '利润']
    series_list = [
        {
            "name": '销量',
            "type": 'bar',
            "data": [10, 25, 40, 60, 30, 20]
        },
        {
            "name": '利润',
            "type": 'bar',
            "data": [15, 40, 70, 100, 55, 35]
        }
    ]
    x_axis_data = ['T恤', '毛衣', '雪纺衫', '裤子', '高跟鞋', '袜子']
    result = {
        'status': True,
        'data': {
            'legend': legend_data,
            'series': series_list,
            'x_axis': x_axis_data
        }
    }
    return JsonResponse(result)
