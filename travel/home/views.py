import json
import traceback

from django.core.paginator import Paginator
from django.db.models import Q, Sum, Count
from django.db.models.functions import TruncDate
from django.http import JsonResponse
from django.shortcuts import render
from fontTools.ttx import process

from .models import TravelInfo

import os
import sys

# 1. 获取当前 views.py 文件的绝对路径（travel/home/views.py）
current_file = os.path.abspath(__file__)
# 2. 获取当前文件所在目录（travel/home/）
current_dir = os.path.dirname(current_file)
# 3. 回退1级到 travel/ 目录（包含 home、user 等app）
travel_core_dir = os.path.dirname(current_dir)
# 4. 回退2级到总根目录（包含 AI、travel、utils 的目录）
root_dir = os.path.dirname(travel_core_dir)

# 5. 添加路径到系统路径（确保能找到 user、utils、AI）
sys.path.append(travel_core_dir)  # 用于导入 user/models.py
sys.path.append(root_dir)         # 用于导入 utils + AI 模块

# 导入AI模块（AI在root_dir目录下）
from AI.Get_Message import Get_DeepSeek

from utils.util import query
from user.models import UserInfo
# Create your views here.

def index(request):
    non_free_count = TravelInfo.objects.exclude(
        Q(actual_price='免费') | Q(actual_price__isnull=True)
    ).count()
    pro_count = TravelInfo.objects.values('province').distinct().count()
    city_count = TravelInfo.objects.values('city').distinct().count()
    total_reviews = TravelInfo.objects.aggregate(
        total_reviews=Sum('review_count')
    )['total_reviews'] or 0

    # 地图数据
    sql = 'select * from part6'
    res = query(sql)
    mapData = [{"name": i[1], "value": i[2]} for i in res]

    # 景区热度排行
    top_5_travel = TravelInfo.objects.all().order_by('-popularity_score')[:5]
    top_10_travel = TravelInfo.objects.all().order_by('-review_count')[:5]

    # 用户创建时间趋势
    daily_users = UserInfo.objects.annotate(
        date=TruncDate('created_at')
    ).values('date').annotate(
        count=Count('id')
    ).order_by('date')

    name_list = [str(item['date']) for item in daily_users]
    value_list = [item['count'] for item in daily_users]
    print(name_list)
    print(value_list)

    content = {
        'non_free_count': non_free_count,
        'pro_count': pro_count,
        'city_count': city_count,
        'total_reviews': total_reviews,
        'mapData': mapData,
        'top_5_travel': top_5_travel,
        'top_10_travel': top_10_travel,
        'name_list': name_list,
        'value_list': value_list,
    }
    return render(request, 'index.html', content)

def travel_list(request):
    # 获取所有省份数据
    provinces = TravelInfo.objects.exclude(province__isnull=True).values_list('province', flat=True).distinct()

    # 初始化查询条件
    travels = TravelInfo.objects.all()

    # 获取搜索条件
    search_name = request.GET.get('search_name', '')
    selected_province = request.GET.get('province', '')

    # 应用筛选条件
    if search_name:
        travels = travels.filter(Q(name__icontains=search_name))

    if selected_province:
        travels = travels.filter(province=selected_province)

    # 排序
    travels = travels.order_by('-popularity_score')

    # 分页
    paginator = Paginator(travels, 10)

    # 获取当前页码
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'provinces': provinces,
        'search_name': search_name,
        'selected_province': selected_province,
    }

    return render(request, 'travel_list.html', context)


def get_ai_travelRoute(request):
    if request.method == "POST":
        try:
            # 修复1：简化JSON解析逻辑（普通Django视图统一解析request.body）
            try:
                # 先解码再解析，兼容所有POST JSON请求
                data = json.loads(request.body.decode('utf-8'))
            except json.JSONDecodeError as e:
                print(f"JSON解析失败: {str(e)}")  # 打印错误日志
                return JsonResponse({
                    'code': 400,
                    'message': f'无效的JSON数据: {str(e)}',
                    'data': None
                })

            # 打印前端传参，方便排查
            print(f"前端传入参数: {data}")

            # 字段检查
            required_fields = ['city', 'season', 'days']
            for field in required_fields:
                if field not in data:
                    return JsonResponse({
                        'code': 400,
                        'message': f'缺少必要字段: {field}',
                        'data': None
                    })

            # 处理预算参数
            budget = data.get('budget', 0)
            if budget == 0 or budget == '0':  # 兼容前端传字符串0的情况
                budget = '不限预算'

            dp = Get_DeepSeek()
            result = dp._get_travel_plan(
                city=data['city'],
                season=data['season'],
                days=data['days'],
                budget=budget
            )

            # 打印AI接口返回结果，排查失败原因
            print(f"AI接口返回结果: {result}")

            if result.get('code') == 200:  # 用get避免key不存在报错
                return JsonResponse({
                    'code': 200,
                    'message': '旅游路线生成成功',
                    'data': result['data']
                })
            else:
                # 返回AI接口的具体错误信息，而非泛泛的“失败”
                error_msg = result.get('message', 'AI接口未返回具体错误')
                return JsonResponse({
                    'code': result.get('code', 400),
                    'message': f'旅游路线生成失败: {error_msg}',
                    'data': None
                })

        except Exception as e:
            # 修复3：打印详细异常栈，方便定位错误
            print(f"服务器内部错误: {str(e)}")
            traceback.print_exc()  # 打印完整的异常调用栈
            return JsonResponse({
                'code': 500,
                'message': f'服务器内部错误: {str(e)}',
                'data': None
            })
    else:
        return render(request, 'get_ai_travelRoute.html')