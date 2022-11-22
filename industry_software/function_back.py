from django.shortcuts import render
from django.shortcuts import redirect
from django.core.paginator import Paginator, Page, EmptyPage, PageNotAnInteger
from myapp import models
from django.db.models import Q
import os.path
import pandas as pd
import json
from industry_software.tools.software_tool import run

MEDIA_ROOT = "/root/industry_software/industry_software/dataset/"
json_file_path = '/root/industry_software/industry_software/dataset/upload.json'

def home(request):
    return render(request, 'home.html')

def back(request):
    return redirect('/')

def detail_back(request):
    guanjian = request.GET.get('guanjian')
    page = request.GET.get('page')
    option_type = request.GET.get('option_type')
    return redirect('/rank/?guanjian='+guanjian+'&page='+page+'&option_type='+option_type)

# 可视化分析
def visual(request):
    return render(request, 'visual.html')

def guangdong(request):
    return render(request, '广东.html')

def shenzhen(request):
    return render(request, '深圳.html')

def guangzhou(request):
    return render(request, '广州.html')

def zhuhai(request):
    return render(request, '珠海.html')

def foshan(request):
    return render(request, '佛山.html')

def dongguang(request):
    return render(request, '东莞.html')

def jiangmen(request):
    return render(request, '江门.html')

def shantou(request):
    return render(request, '汕头.html')

def huizhou(request):
    return render(request, '惠州.html')

def zhongshan(request):
    return render(request, '中山.html')

def maoming(request):
    return render(request, '茂名.html')

def qingyuan(request):
    return render(request, '清远.html')

def zhaoqing(request):
    return render(request, '肇庆.html')

def yangjiang(request):
    return render(request, '阳江.html')

def heyuan(request):
    return render(request, '河源.html')

def yunfu(request):
    return render(request, '云浮.html')

def zhanjiang(request):
    return render(request, '湛江.html')

def jieyang(request):
    return render(request, '揭阳.html')

def shanwei(request):
    return render(request, '汕尾.html')

def shaoguan(request):
    return render(request, '韶关.html')

def meizhou(request):
    return render(request, '梅州.html')

def chaozhou(request):
    return render(request, '潮州.html')

def gohome(request):
    return redirect('/')

# 排行榜
def rank(request):
    # 获取排行榜关键字信息
    if request.method == 'POST':
        text = request.POST.get('uptext')
        option_type = request.POST.get('option_type')
        contact_list = models.Rank.objects.filter(Q(type=option_type)&(Q(name__contains=text)|Q(range__contains=text))).order_by('-score')  # 这边的Rank指代数据表
        paginator = Paginator(contact_list, 15)  # 15是每页显示的数量，把数据库取出的数据生成paginator对象，并指定每页显示的数量
        page = request.GET.get('page')  # 从查询字符串获取page的当前页数
        print('----------------------------上传时关键字查询过程' + str(page))
        if page:  # 判断：获取当前页码的数据集，这样在模版就可以针对当前的数据集进行展示
            data_list = paginator.page(page).object_list
        else:
            data_list = paginator.page(1).object_list
        try:  # 实现分页对象，分别判断当页码存在/不存在的情况，返回当前页码对象
            page_object = paginator.page(page)
        except PageNotAnInteger:
            page_object = paginator.page(1)
        except EmptyPage:
            page_object = paginator.page(paginator.num_pages)
        return render(request, 'rank.html', {'page_object': page_object, 'data_list': data_list, 'number': (page_object.number - 1) * 15, 'guanjian': text, 'option_type': option_type})
    elif request.method == 'GET':
        guanjian = request.GET.get('guanjian')
        option_type = request.GET.get('option_type')
        if not option_type:
            option_type = '工业软件研发'
        # 无关键字查询的信息
        if not guanjian:
            # 从Django自带的paginator模块插入类
            contact_list = models.Rank.objects.filter(Q(type=option_type)).order_by('-score')  # 这边的model指代数据表
            paginator = Paginator(contact_list, 15)  # 15是每页显示的数量，把数据库取出的数据生成paginator对象，并指定每页显示的数量
            page = request.GET.get('page')  # 从查询字符串获取page的当前页数
            print('----------------------------无关键字查询过程'+str(page))
            if page:  # 判断：获取当前页码的数据集，这样在模版就可以针对当前的数据集进行展示
                data_list = paginator.page(page).object_list
            else:
                data_list = paginator.page(1).object_list
            try:  # 实现分页对象，分别判断当页码存在/不存在的情况，返回当前页码对象
                page_object = paginator.page(page)
            except PageNotAnInteger:
                page_object = paginator.page(1)
            except EmptyPage:
                page_object = paginator.page(paginator.num_pages)
            return render(request, 'rank.html', {'page_object': page_object, 'data_list': data_list, 'number': (page_object.number - 1) * 15, 'page': page, 'option_type': option_type})
        # 查完详情后返回不重刷新
        else:
            contact_list = models.Rank.objects.filter(Q(type=option_type)&(Q(type__contains=guanjian) | Q(range__contains=guanjian))).order_by('-score')  # 这边的model指代数据表
            paginator = Paginator(contact_list, 15)  # 15是每页显示的数量，把数据库取出的数据生成paginator对象，并指定每页显示的数量
            page = request.GET.get('page')  # 从查询字符串获取page的当前页数
            print('----------------------------关键字查询过程' + str(page))
            if page:  # 判断：获取当前页码的数据集，这样在模版就可以针对当前的数据集进行展示
                data_list = paginator.page(page).object_list
            else:
                data_list = paginator.page(1).object_list
            try:  # 实现分页对象，分别判断当页码存在/不存在的情况，返回当前页码对象
                page_object = paginator.page(page)
            except PageNotAnInteger:
                page_object = paginator.page(1)
            except EmptyPage:
                page_object = paginator.page(paginator.num_pages)
            return render(request, 'rank.html', {'page_object': page_object, 'data_list': data_list, 'number': (page_object.number - 1) * 15, 'guanjian': guanjian, 'page': page, 'option_type': option_type})

def getDetail(request):
    rank_id = request.GET.get('rank_id')
    guanjian = request.GET.get('guanjian')
    page = request.GET.get('page')
    option_type = request.GET.get('option_type')
    data = models.Rank.objects.get(rank_id=rank_id)
    return render(request, 'detail.html', {'rank_id': rank_id, 'guanjian': guanjian, 'data': data, 'page': page, 'option_type': option_type})


from io import BytesIO
from django.http import HttpResponse
import xlwt

# 导出查询的数据
def export_data(request):

    # 设置HTTPResponse的类型
    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment;filename=order.xls'
    # 创建一个文件对象
    wb = xlwt.Workbook(encoding='utf8')
    # 创建一个sheet对象
    sheet = wb.add_sheet('order-sheet')

    # 设置文件头的样式,这个不是必须的可以根据自己的需求进行更改
    style_heading = xlwt.easyxf("""
                font:
                    name Arial,
                    colour_index white,
                    bold on,
                    height 0xA0;
                align:
                    wrap off,
                    vert center,
                    horiz center;
                pattern:
                    pattern solid,
                    fore-colour 0x19;
                borders:
                    left THIN,
                    right THIN,
                    top THIN,
                    bottom THIN;
                """)

    # 写入文件标题
    sheet.write(0, 0, '编号', style_heading)
    sheet.write(0, 1, '名称', style_heading)
    sheet.write(0, 2, '资产总额', style_heading)
    sheet.write(0, 3, '营业收入', style_heading)
    sheet.write(0, 4, '净资产收益率', style_heading)
    sheet.write(0, 5, '科技创新总含量', style_heading)
    sheet.write(0, 6, '注册资本', style_heading)
    sheet.write(0, 7, '产品', style_heading)
    sheet.write(0, 8, '经营范围', style_heading)
    sheet.write(0, 9, '简介', style_heading)
    sheet.write(0, 10, '得分', style_heading)
    sheet.write(0, 11, '类型', style_heading)


    # 写入数据
    data_row = 1
    # UserTable.objects.all()这个是查询条件,可以根据自己的实际需求做调整.
    for i in models.Rank.objects.all():
        sheet.write(data_row, 0, i.rank_id)
        sheet.write(data_row, 1, i.name)
        sheet.write(data_row, 2, i.assets)
        sheet.write(data_row, 3, i.income)
        sheet.write(data_row, 4, i.yield_rate)
        sheet.write(data_row, 5, i.total_content)
        sheet.write(data_row, 6, i.capital)
        sheet.write(data_row, 7, i.product)
        sheet.write(data_row, 8, i.range)
        sheet.write(data_row, 9, i.Introduction)
        sheet.write(data_row, 10, i.score)
        sheet.write(data_row, 11, i.type)

        data_row = data_row + 1

    # 写出到IOr
    output = BytesIO()
    wb.save(output)
    # 重新定位到开始
    output.seek(0)
    response.write(output.getvalue())
    return response


# 文件上传
def upload(request):
    if request.method == 'POST':
  
        # 读取单选框的类别内容
        button_type = request.POST.get('type')
    
        # 保存上传的文件
        file = request.FILES['upfile']

        filename = os.path.join(MEDIA_ROOT, 'upload.xlsx')
        if file.name.split('.')[1] not in ['xlsx']:
            return render(request, 'upload.html', {'alarm': '请上传正确的xlsx格式文件'})
        # try:

        with open(filename, 'wb') as f:
            f.write(file.read())

        # 读取上传的文件+数据表查询的内容
        df = pd.read_excel(filename)

        doc_list = []
        for index, row in df.iterrows():
            row_list = []
            row_list.append(row[0])
            row_list.append(row[1])
            row_list.append(row[2])
            row_list.append(row[3])
            row_list.append(row[4])
            row_list.append(row[5])
            row_list.append(row[6])
            doc_list.append(row_list)

        contact_list = models.Rank.objects.filter(Q(type=button_type))
        for i in contact_list:
            row_list = []
            row_list.append(i.name)
            row_list.append(i.assets)
            row_list.append(i.income)
            row_list.append(i.yield_rate)
            row_list.append(i.total_content)
            row_list.append(i.capital)
            row_list.append(i.product)
            doc_list.append(row_list)

        with open(json_file_path, 'w', encoding='utf-8') as f:
            json.dump(doc_list, f, indent=4, ensure_ascii=False)

        run(button_type)

        # os.remove(json_file_path)
        # os.remove(filename)

        # 读取数据库的数据进行比较,重复则删除重复上传的内容
        '''for index, row in df.iterrows():
            for i in models.Rank.objects.filter(Q(type__contains=button_type)):
                if(row["名称"] == i.name):
                    df.drop(index, inplace=True)'''

        df_score = pd.read_excel('/root/industry_software/industry_software/dataset/upload_score.xlsx')
        # 将数据添加到数据库
        for index, row in df_score.iterrows():
            rank = models.Rank()
            rank.name = row[0]
            rank.assets = row[1]
            rank.income = row[2]
            rank.yield_rate = row[3]
            rank.total_content = row[4]
            rank.capital = row[5]
            rank.product = row[6]
            rank.range = row[7]
            rank.Introduction = row[8]
            rank.score = row[9]
            rank.type = button_type
            rank.save()

        os.remove('/root/industry_software/industry_software/dataset/upload_score.xlsx')

        return render(request, 'upload.html', {'alarm': '上传成功'})

        # except:
        #     return render(request, 'upload.html', {'alarm': 'excel表格的内容填写，请参照原样本的格式'})
    else:

        return render(request, 'upload.html', {})

# admin后端展示数据表, 正常使用建议注释
# 而在def函数中有出现modes.Expert调用后, admin一样可以展示
from django.contrib import admin
admin.site.register(models.Expert)

#
def expert(request):

    return render(request, '', {})
