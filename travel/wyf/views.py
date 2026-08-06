from django.http import JsonResponse
from django.shortcuts import render
from select import select

from utils import util

# Create your views here.
def part1(request):
    sql1 = "select * from part1"
    res = util.query(sql1)
    data_list = [{"value": i[2], "name": i[1]} for i in res]

    sql2 = "select * from part8"
    res2 = util.query(sql2)

    name_list = [i[1] for i in res2]
    travel_num_list = [i[2] for i in res2]
    avg_score_list = [i[3] for i in res2]

    content = {
        'data_list': data_list,
        'name_list': name_list,
        'travel_num_list': travel_num_list,
        'avg_score_list': avg_score_list,
    }
    return render(request, 'wyf/part1.html', content)

def part2(request):
    sql1 = "select * from part2"
    res = util.query(sql1)
    name_list = [i[1] for i in res]
    data_list = [{"value": i[2], "name": i[1]} for i in res]

    sql2 = "select distinct city from part7"
    res2 = util.query(sql2)
    select_list = [i[0] for i in res2]

    content = {
        'data_list':data_list,
        'name_list':name_list,
        'select_list':select_list,
    }
    return render(request, 'wyf/part2.html', content)

def get_cityData(request):
    city = request.GET.get('city', '')
    sql = f"select name,value from part7 where city='{city}'"
    res = util.query(sql)

    name_list = [i[0] for i in res]
    value_list = [i[1] for i in res]

    name_list = name_list[::-1]
    value_list = value_list[::-1]

    content = {
        'names': name_list,
        'values': value_list,
    }
    return JsonResponse({"data": content})

def part3(request):
    sql = "select * from part3"
    res = util.query(sql)
    name_list = [i[1] for i in res]
    value_list = [i[2] for i in res]

    content = {
        'name_list':name_list,
        'value_list':value_list,
    }
    return render(request, 'wyf/part3.html', content)

def part4(request):
    sql = "select * from part4"
    res = util.query(sql)
    data_list = [{"name": i[1], "value": i[2]} for i in res]

    content = {
        'data_list':data_list,
    }
    return render(request, 'wyf/part4.html', content)

def part5(request):
    sql = "select * from part5"
    res = util.query(sql)
    data_list = [{"value": i[2], "name": i[1]} for i in res]

    content = {
        'data_list':data_list,
    }
    return render(request, 'wyf/part5.html', content)

def part6(request):
    # 地图数据
    sql = 'select * from part6'
    res = util.query(sql)
    mapData = [{"name": i[1], "value": i[2]} for i in res]
    content = {
        'mapData':mapData,
    }
    return render(request, 'wyf/part6.html', content)