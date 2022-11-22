# 前7行代码构建一个django配置，仅仅为了在单个python文件能够运行，测试下对数据库db.sqlite3的Rank表进行操作。
import sys
sys.path.append(r'E:\Python\industry_software')
import django
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "industry_software.settings")
django.setup()

import xlrd
from threading import Thread
from myapp import models

# 为了方便测试,上传一份列表，可以对原先列表的信息进行删减或增加，来生成不同的竞争力分数
data_path = r"E:\Python\industry_software\industry_software\dataset\data.xls"

# 读取excel
excel_data = xlrd.open_workbook(data_path)

# 这里是读公司表以及排行榜表的函数
def read_rank(sheet):
    row =sheet.nrows
    print(row)
    # 读取表格数据存入数据库中（order-sheet）
    for row in range(1,row):
        rank = models.Rank()
        company = models.Company()
        company.name = sheet.cell(row, 0).value
        company.assets = sheet.cell(row, 1).value
        company.income = sheet.cell(row, 2).value
        company.yield_rate = sheet.cell(row, 3).value
        company.total_content = sheet.cell(row, 4).value
        company.capital = sheet.cell(row, 5).value
        company.fz_product = sheet.cell(row, 6).value
        company.qr_product = sheet.cell(row, 7).value
        company.kz_product = sheet.cell(row, 8).value
        company.jy_product = sheet.cell(row, 9).value
        company.pt_product = sheet.cell(row, 10).value
        company.product_num = sheet.cell(row, 11).value
        company.range = sheet.cell(row, 12).value
        company.Introduction = sheet.cell(row, 13).value

        rank.name = sheet.cell(row, 0).value
        rank.score = sheet.cell(row, 14).value
        rank.type = sheet.cell(row, 15).value

        rank.save()
        company.save()
    print("读取成功")

sheet = excel_data.sheets()[0]
# 这里设置线程函数
thread1 = Thread(target=read_rank, args=(sheet,))
thread1.start()


# 这里是读公司产品的函数
def read_product(sheet):
    # ctype: 0empty, 1string, 2number, 3date, 4boolean, 5error
    # 这里开发读产品明细代码
    # 获取表格总行数
    rows = sheet.nrows
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

sheet = excel_data.sheets()[1]
# 这里设置线程函数
thread2 = Thread(target=read_product, args=(sheet,))
thread2.start()