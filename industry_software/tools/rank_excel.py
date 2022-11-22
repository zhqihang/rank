import xlrd
import json
import pandas as pd

data_path = r"/root/industry_software/industry_software//dataset/工业软件研发.xlsx"

# 排序
xl = pd.read_excel(data_path, index_col=0)
xl = xl.sort_values(by="topcis法", ascending=False)
xl.to_excel(data_path)

# 读取成json格式
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
            values = self.sheet.row_values(i)
            datas.append(
                (
                    {
                        "rank": i,
                        "name": str(values[0]),
                        "topic": values[9],
                    }
                )
            )
        return datas


sheet_name = "Sheet1"
excel_utils = Excel_util(data_path, sheet_name)
datas = excel_utils.read_excel()
print(datas)
# js = json.dumps(datas, sort_keys=False, ensure_ascii=False, indent=4, separators=(',', ':'))
# print(js)




