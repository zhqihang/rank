# _*_ codeing : utf-8 _*_
# @Time: 2022/12/4 16:09
# @Author: zqh
# @File: read_excel
# @Project: industry_software
import sys
sys.path.append(r'E:\Python\industry_software')
import django
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "industry_software.settings")
django.setup()

import xlrd
from threading import Thread
from myapp import models
from django.db.models import Q

# excel文件路径
data_path = r"E:\Python\industry_software\industry_software\dataset\工业软件排行总表.xls"
# 读取excel文件
excel_data = xlrd.open_workbook(data_path)

# 这里的开发依赖Excel的表格格式
def read_excel(excel):
    # 总产品sheet
    sheet_zcp = excel.sheets()[5]
    row_zcp =sheet_zcp.nrows
    print(row_zcp)
    company = models.Company()
    # 读取表格数据存入数据库中（"总产品"）
    for row in range(1,row_zcp):
        company.name = sheet_zcp.cell(row, 0).value # 公司名
        company.total_content = sheet_zcp.cell(row,1).value # 科技创新总含量
        company.capital = sheet_zcp.cell(row,2).value # 注册资本
        company.product_num = sheet_zcp.cell(row,3).value # 总产品数
        company.Introduction = sheet_zcp.cell(row,5).value # 公司简介
        company.range = sheet_zcp.cell(row,6).value # 经营范围
        company.pos_neg = sheet_zcp.cell(row,7).value # topcis法得分（总得分），暂存在pos_neg字段
        company.save()
    print("读取成功")

    # 各类型sheet
    sheet_fz = excel_data.sheets()[0]
    sheet_qr = excel_data.sheets()[1]
    sheet_kz = excel_data.sheets()[2]
    sheet_jy = excel_data.sheets()[3]
    sheet_pt = excel_data.sheets()[4]
    # 读取数据到排行榜表格中
    # 工业仿真设计表
    rank = models.Rank()
    row_fz = sheet_fz.nrows
    for row in range(1,row_fz):
        rank.name = sheet_fz.cell(row,0).value # 公司名
        # 单个产品数写入公司表的对应字段
        if models.Company.objects.filter(Q(name=sheet_fz.cell(row,0).value)):
            print("一致")
            company = models.Company.objects.get(Q(name=sheet_fz.cell(row, 0).value))
            company.fz_product = sheet_fz.cell(row,3).value
            company.save()
        rank.score = sheet_fz.cell(row,8).value # topcis分数
        rank.type = sheet_fz.cell(row,9).value # 类型
        rank.save()
    # 工业嵌入式表
    row_qr = sheet_qr.nrows
    for row in range(1,row_qr):
        rank.name = sheet_qr.cell(row,0).value # 公司名
        # 单个产品数写入公司表的对应字段
        if models.Company.objects.filter(Q(name=sheet_qr.cell(row,0).value)):
            company = models.Company.objects.get(Q(name=sheet_qr.cell(row,0).value))
            print("一致")
            company.qr_product = sheet_qr.cell(row,3).value
            company.save()
        rank.score = sheet_qr.cell(row,8).value # topcis分数
        rank.type = sheet_qr.cell(row,9).value # 类型
        rank.save()
    # 工业生产控制表
    row_kz = sheet_kz.nrows
    for row in range(1,row_kz):
        rank.name = sheet_kz.cell(row,0).value # 公司名
        # 单个产品数写入公司表的对应字段
        if models.Company.objects.filter(Q(name=sheet_kz.cell(row,0).value)):
            print("一致")
            company = models.Company.objects.get(Q(name=sheet_kz.cell(row, 0).value))
            company.kz_product = sheet_kz.cell(row,3).value
            company.save()
        rank.score = sheet_kz.cell(row,8).value # topcis分数
        rank.type = sheet_kz.cell(row,9).value # 类型
        rank.save()
    # 工业经营管理表
    row_jy = sheet_jy.nrows
    for row in range(1,row_jy):
        rank.name = sheet_jy.cell(row,0).value # 公司名
        # 单个产品数写入公司表的对应字段
        if models.Company.objects.filter(Q(name=sheet_jy.cell(row,0).value)):
            print("一致")
            company = models.Company.objects.get(Q(name=sheet_jy.cell(row, 0).value))
            company.jy_product = sheet_jy.cell(row,3).value
            company.save()
        rank.score = sheet_jy.cell(row,8).value # topcis分数
        rank.type = sheet_jy.cell(row,9).value # 类型
        rank.save()
    # 工业平台与系统
    row_pt = sheet_pt.nrows
    for row in range(1,row_pt):
        rank.name = sheet_pt.cell(row,0).value # 公司名
        # 单个产品数写入公司表的对应字段
        if models.Company.objects.filter(Q(name=sheet_pt.cell(row,0).value)):
            print("一致")
            company = models.Company.objects.get(Q(name=sheet_pt.cell(row, 0).value))
            company.pt_product = sheet_pt.cell(row,3).value
            company.save()
        rank.score = sheet_pt.cell(row,8).value # topcis分数
        rank.type = sheet_pt.cell(row,9).value # 类型
        rank.save()

# 设置线程函数
# thread = Thread(target=read_excel, args=(excel_data,))
# thread.start()


# 这里是读公司产品的函数
def read_product(sheet):
    # ctype: 0empty, 1string, 2number, 3date, 4boolean, 5error
    # 这里开发读产品明细代码
    # 获取表格总行数
    rows = sheet.nrows
    print(rows)
    # 初始化变量
    start_index = 0
    end_index = 0
    i = 1
    # 读表格数据
    for item in range(1, rows):
        products = models.Products()
        # 如果单元格内容不为空
        if sheet.cell(item, 0).ctype != 0:
            # 当单元格内容为公司名
            if sheet.cell(item, 0).value != "SUM":
                start_index = item
            else:
                # 考虑这里和range(),item不用-1
                end_index = item
        if start_index < end_index:
        # 循环获取所有数据
            print("开始读从第{}开始，到{}行结束的数据".format(start_index, end_index))
            for col in range(1, 6):
                for row in range(start_index, end_index):
                    if sheet.cell(row, col).ctype != 0:
                        products.pro_id = i
                        products.pro_company = sheet.cell(start_index, 0).value
                        products.pro_detail = sheet.cell_value(row, col)
                        products.pro_type = col
                        i = i + 1
                        products.save()
        else:
            continue

sheet = excel_data.sheets()[6]
# 这里设置线程函数
thread2 = Thread(target=read_product, args=(sheet,))
thread2.start()