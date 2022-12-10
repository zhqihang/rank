from django.shortcuts import render,HttpResponse
from myapp import models
from django.db.models import Q
from django.http import JsonResponse

# Create your views here.

# 这里开发首页竞争力可视化
def visualize(request):
    # 获取公司对象
    company = models.Company.objects.all()
    return render(request,"visualize.html",{"company":company})

def keshihua(request):
    name = request.GET.get('name')
    # 根据用户点击的公司名查询数据库表，返回该公司对象
    company = models.Company.objects.get(Q(name=name))
    rank= models.Rank.objects.get(Q(name=name))
    print(company)
    return render(request, "keshihua.html", {"name":name, "com":company, "rank":rank})


def chart_zhexian(request):
    x_axis_data=[]
    company = models.Company.objects.all()
    for item in company:
        x_axis_data.append(item.name)
    x_axis_list=x_axis_data[:20]

    y_axis = [
            {
              'name': '产品研发类',
              'type': 'line',

              'data': [118, 233, 170, 139, 145, 155, 232, 162, 202, 297, 125, 251, 178, 118, 114, 152, 170, 220, 187, 235]
            },
            {
              'name': '嵌入式类',
              'type': 'line',

              'data':[298, 395, 292, 379, 398, 248, 325, 218, 265, 307, 369, 338, 346, 287, 350, 379, 279, 370, 287, 225]
            },
            {
              'name': '生产控制类',
              'type': 'line',

              'data': [730, 799, 645, 620, 662, 681, 706, 615, 757, 743, 781, 636, 649, 611, 761, 698, 785, 705, 778, 741]
            },
            {
              'name': '信息管理类',
              'type': 'line',

              'data': [665, 677, 689, 740, 542, 549, 771, 684, 506, 606, 586, 690, 777, 653, 634, 510, 608, 524, 580, 554]
            },
            {
              'name': '平台与系统类',
              'type': 'line',

              'data': [946, 786, 710, 717, 613, 693, 903, 875, 843, 754, 747, 928, 615, 950, 995, 986, 994, 678, 978, 637]
            }
          ]

    result = {
        "status":True,
        "data":{
            "x_axis":x_axis_list,
            "y_axis":y_axis,
        }
    }
    return JsonResponse(result)
from django.shortcuts import render,HttpResponse
from myapp import models
from django.db.models import Q

# Create your views here.

# 这里开发首页竞争力可视化
def visualize(request):
    # 获取公司对象
    company = models.Company.objects.all()
    return render(request,"visualize.html",{"company":company})

def keshihua(request):
    name = request.GET.get('name')
    # 根据用户点击的公司名查询数据库表，返回该公司对象
    company = models.Company.objects.get(Q(name=name))
    print(company)
    return render(request, "keshihua.html", {"name":name, "com":company})