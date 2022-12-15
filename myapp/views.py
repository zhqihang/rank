from django.shortcuts import render,HttpResponse
from myapp import models
from django.db.models import Q
from django.http import JsonResponse

# Create your views here.

# 这里开发首页竞争力可视化
def visualize(request):
    return render(request,"visualize.html")
#
# def keshihua(request):
#     name = request.GET.get('name')
#     # 根据用户点击的公司名查询数据库表，返回该公司对象
#     company = models.Company.objects.get(Q(name=name))
#     rank= models.Rank.objects.get(Q(name=name))
#     print(company)
#     return render(request, "keshihua.html", {"name":name, "com":company, "rank":rank})


def chart_zhexian(request):
    x_axis_data=[]
    y_axis_fz_data = []
    y_axis_qr_data = []
    y_axis_kz_data = []
    y_axis_jy_data = []
    y_axis_pt_data = []
    company = models.Company.objects.all()
    for item in company:
        x_axis_data.append(item.name)
        y_axis_fz_data.append(item.fz_product)
        y_axis_qr_data.append(item.qr_product)
        y_axis_kz_data.append(item.kz_product)
        y_axis_jy_data.append(item.jy_product)
        y_axis_pt_data.append(item.pt_product)
    x_axis_list=x_axis_data[:20]
    y_axis_fz_list = y_axis_fz_data[:20]
    y_axis_qr_list = y_axis_qr_data[:20]
    y_axis_kz_list = y_axis_kz_data[:20]
    y_axis_jy_list = y_axis_jy_data[:20]
    y_axis_pt_list = y_axis_pt_data[:20]
    y_axis = [
            {
              'name': '产品研发类',
              'type': 'line',
              'data': y_axis_fz_list
            },
            {
              'name': '嵌入式类',
              'type': 'line',
              'data':y_axis_qr_list
            },
            {
              'name': '生产控制类',
              'type': 'line',
              'data': y_axis_kz_list
            },
            {
              'name': '信息管理类',
              'type': 'line',
              'data': y_axis_jy_list
            },
            {
              'name': '平台与系统类',
              'type': 'line',
              'data': y_axis_pt_list
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

#百度地图
def baiduMap(request):
    return render(request, 'baiduMap.html')

def baiduMapv(request):
    return render(request, 'baiduMapv.html')