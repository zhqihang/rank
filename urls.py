# """industry_software URL Configuration
#
# The `urlpatterns` list routes URLs to views. For more information please see:
#     https://docs.djangoproject.com/en/3.1/topics/http/urls/
# Examples:
# Function views
#     1. Add an import:  from my_app import views
#     2. Add a URL to urlpatterns:  path('', views.home, name='home')
# Class-based views
#     1. Add an import:  from other_app.views import Home
#     2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
# Including another URLconf
#     1. Import the include() function: from django.urls import include, path
#     2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
# """

from django.contrib import admin
from django.urls import path
from industry_software import function
from myapp import views

# from myapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', function.home),
    # path('back/', function.back),
    # path('visual/', function.visual),
    # path('visual/back/', function.back),

    path('rank/back/', function.back),
    path('rank/', function.rank),
    path('rank/detail/', function.getDetail),
    path('rank/detail/back/', function.detail_back),

    path('upload/', function.upload),
    path('upload/back/', function.back),
    path('export_data/',function.export_data),

    path('guangdong/', function.guangdong),
    path('guangdong/vi', function.gohome),
    path('shenzhen/', function.shenzhen),
    path('shenzhen/vi', function.gohome),
    path('guangzhou/', function.guangzhou),
    path('guangzhou/vi', function.gohome),
    path('zhuhai/', function.zhuhai),
    path('zhuhai/vi', function.gohome),
    path('foshan/', function.foshan),
    path('foshan/vi', function.gohome),
    path('dongguang/', function.dongguang),
    path('dongguang/vi', function.gohome),
    path('jiangmen/', function.jiangmen),
    path('jiangmen/vi', function.gohome),
    path('shantou/', function.shantou),
    path('shantou/vi', function.gohome),
    path('huizhou/', function.huizhou),
    path('huizhou/vi', function.gohome),
    path('zhongshan/', function.zhongshan),
    path('zhongshan/vi', function.gohome),
    path('maoming/', function.maoming),
    path('maoming/vi', function.gohome),
    path('qingyuan/', function.qingyuan),
    path('qingyuan/vi', function.gohome),
    path('zhaoqing/', function.zhaoqing),
    path('zhaoqing/vi', function.gohome),
    path('yangjiang/', function.yangjiang),
    path('yangjiang/vi', function.gohome),
    path('heyuan/', function.heyuan),
    path('heyuan/vi', function.gohome),
    path('yunfu/', function.yunfu),
    path('yunfu/vi', function.gohome),
    path('zhanjiang/', function.zhanjiang),
    path('zhanjiang/vi', function.gohome),
    path('jieyang/', function.jieyang),
    path('jieyang/vi', function.gohome),
    path('shanwei/', function.shanwei),
    path('shanwei/vi', function.gohome),
    path('shaoguan/', function.shaoguan),
    path('shaoguan/vi', function.gohome),
    path('meizhou/', function.meizhou),
    path('meizhou/vi', function.gohome),
    path('chaozhou/', function.chaozhou),
    path('chaozhou/vi', function.gohome),

    # 这里是首页竞争力可视化
    path('visualize/', views.visualize),
    path('visualize/vi',function.gohome),
    path('visualize/keshihua', views.keshihua),
    path('visualize/chart/',views.chart_zhexian),

    #百度地图
    path('baiduMap/', views.baiduMap),
    path('baiduMapv/', views.baiduMapv),
]
