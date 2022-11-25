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
    rank= models.Rank.objects.get(Q(name=name))
    print(company)
    return render(request, "keshihua.html", {"name":name, "com":company, "rank":rank})