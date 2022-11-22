# -*- encoding: utf-8 -*-
'''
@File   ：read_excel.py
@Time   ：2020/7/3 22:19
@Author : zdc
'''
import xlrd
import json


class Excel_util():

    def __init__(self, data_path, sheet_name):
        """
        :param data_path: 文件路径
        :param sheet_name: excel中sheet的名称
        """
        # excel存放的工作路径
        self.data_path = data_path
        # excel表的名称
        self.sheet_name = sheet_name
        # 读取excel表返回一个data对象
        self.data = xlrd.open_workbook(data_path)
        # 利用data对象返回一个sheet对象
        self.sheet = self.data.sheet_by_name(sheet_name)
        # 读取sheet表中第一行的数据的第一个标签,row_values(0)以列表形式返回
        self.company_tag = self.sheet.row_values(0)[0]
        # 读取sheet表的有效行数
        self.rowsNum = self.sheet.nrows
        # 读取sheet表的有效列数
        self.columnsNum = self.sheet.ncols


    def read_excel(self):
        """
        :return: 返回一个列表
        """

        datas = []
        for i in range(1, self.rowsNum):
            data = []
            data.append(self.sheet.cell_value(i, 0))
            for j in range(1, 7):
                data.append(self.sheet.cell_value(i, j))

            datas.append(data)

        return datas


if __name__ == '__main__':
    file_path = r"D:\研究生\工业软件排名\第二次排名\工业软件研发.xlsx"
    sheet_name = "Sheet1"
    excel_utils = Excel_util(file_path, sheet_name)
    datas = excel_utils.read_excel()
    print(datas)
    print(len(datas))

    # 将列表保存至json文件
    with open(r"D:\研究生\工业软件排名\第二次排名\工业软件研发.json", 'w', encoding='utf-8') as f:
        json.dump(datas, f, ensure_ascii=False)