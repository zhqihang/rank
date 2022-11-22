# -*- encoding: utf-8 -*-
'''
@File   ：tool.py
@Time   ：2020/8/11 17:35
@Author : zdc
'''
import numpy as np
np.seterr(divide='ignore',invalid='ignore')
import pandas as pd
import json
from myapp import models
from django.db.models import Q

def countWeight_two(df_new, button_type):
    f = lambda x: (x - x.min()) / (x.max() - x.min()) if x.max() > x.min() else 1.0
    df_new = df_new.apply(f)  # 数据标准化

    # positive_two = positive_two.apply(f)  # 数据标准化
    # # f_two = lambda x: (x.max() - x) / (x.max() - x.min()) if x.min() < 10000000 else ((x - x.min()) / (x.max() - x.min()))
    # neutral_max = neutral.max()
    # neutral_min = neutral.min()
    # registered_capital = 1000000000
    # for index, row in neutral.iterrows():
    #     print(row)
    #     if row.values[0] >= registered_capital:
    #         row.values[0] = (neutral_max - row.values[0]) / (neutral_max - neutral_min)
    #     else:
    #         row.values[0] = (row.values[0] - neutral_min) / (neutral_max - neutral_min)
    #     print(row)
    # df_new = pd.concat([positive, neutral, positive_two], axis=1)
    # print(df_new)

    m = df_new.shape[0]
    df = df_new.iloc[:, :].values
    k = 1 / np.log(m)
    yij = df.sum(axis=0)
    print(yij)
    pij = df / yij  # 计算pij
    test = pij * np.log(pij)
    test = np.nan_to_num(test)
    ej = -k * (test.sum(axis=0))  # 计算每种指标的信息熵
    wi = (1 - ej) / np.sum(1 - ej)  # 计算每种指标的权重
    print('熵权法客观生成')
    print(wi)

    yij_w = yij * [1, 1, 1e-2, 1, 1, 1, 10, 2]
    print('主观赋权') # [1, 1, 1e-1, 1, 1, 2, 40, 5]
    print(yij_w)
    sum_yij = (yij_w).sum(axis=0)
    wi_2 = yij_w / sum_yij
    print('指标归一化')
    print(wi_2)
    if button_type == '工业软件嵌入式':
        wi_combine = wi + wi_2 + [0, 0, 0, 0, 0, 0, 1000000, 1]
    elif button_type == '工业软件研发':
        wi_combine = wi + wi_2 + [0, 0, 0, 0, 0, 0, 5, 1]
    elif button_type == '工业软件生产控制':
        wi_combine = wi + wi_2 + [0, 0, 0, 0, 0, 0, 10, 2]
    elif button_type == '工业软件信息管理':
        wi_combine = wi + wi_2 + [0, 0, 0, 0, 0, 0, 3, 1]
    print('合并')
    print(wi_combine)
    return wi_combine


# entropy weight method
def entropyWeight(data, weight,index):
    res = (data * weight).sum(axis=1).round(2) # 计算最终结果
    df_res=pd.DataFrame(res,columns=[index])
    df_res=df_res.reset_index()
    return df_res

# topsis method
def topsis(data, weight,index):
    data = data / np.sqrt((data ** 2).sum())  # 归一化
    Z = pd.concat([data.min(), data.max()], keys=['负理想解', '正理想解'])
    # Z = pd.concat([data.min(), data.max()], keys=['负理想解', '正理想解'])      # （代替下面报错的代码）
    # Z = pd.DataFrame([data.min(), data.max()], index=['负理想解', '正理想解'])  # 最优最劣方案  #（会报错）
    result = data.copy()
    result['正理想解'] = np.sqrt(((data - Z.loc['正理想解']) ** 2 * weight).sum(axis=1))
    result['负理想解'] = np.sqrt(((data - Z.loc['负理想解']) ** 2 * weight).sum(axis=1))
    result[index] = result['负理想解'] / (result['负理想解'] + result['正理想解'])  # 综合得分指数
    df_res = pd.DataFrame(result[index].round(4), columns=[index])
    df_res = df_res.reset_index()
    return df_res

def read_MyJson(path):
    with open(path, 'r', encoding="utf-8")as f:
        data = json.load(f)
        print(data)
        return data

# def read_Mytxt(path):
#     file = open(path, mode='r', encoding='utf-8')
#     doc_list = []
#     contents = file.readlines()
#     for msg in contents:
#         msg = msg.strip('\n')
#         adm = msg.split(' ')
#         doc_list.append(adm)
#     file.close()
#     return doc_list

# json to df
# def my_JsonNormalize(data,record_path,meta):
#     try:
#         df=pd.json_normalize(data=data,record_path=record_path,meta=meta)
#     except Exception as e:
#         print('my_JsonNormalizem的错误是',e)
#     else:
#         return df

# dataframe merge
# def my_merge(left,right,on):
#     try:
#         df=pd.merge(left=left,right=right,on=on)
#     except Exception as e:
#         print('my_merge的错误是',e)
#     else:
#         return df

# if __name__ == '__main__':

    # -----------------测试样例----------------
    # stu = [['学生5', 150424926.5, -90.56, 80, 14, 15, -16], ['学生3', 97, 89, 93, 14.453, 51, 57], ['学生13', 88, 98.56, 95, 14, 46, 57], ['学生7', 77, 100, 78.456, 34, 68, 797], ['学生2', 80, 96, 94, 2, 3456, 56]]
    # stu = pd.DataFrame(stu,columns=['name', 'math', 'sport', 'fujia1', 'fuijia2', 'fujia3', 'fujia4'])
    # stu.set_index('name',inplace=True)
    # wi=countWeight(stu)
    # df_res=topsis(stu,wi,'topsis法')
    # # df_res=entropyWeight(stu,wi,'熵权法')
    # print(df_res)
    # ----------------------------------
def run(button_type):
    # 载入json文件
    datas = read_MyJson("/root/industry_software/industry_software/dataset/upload.json")
    uplaod_file = "/root/industry_software/industry_software/dataset/upload.xlsx"
    uplaod_file_score = "/root/industry_software/industry_software/dataset/upload_score.xlsx"

    datas_frame = pd.DataFrame(datas, columns=['compang_name', 'total_assets', 'operating_income','rate', 'technological',
                                               'registered_capital', 'product', 'profession_name', 'pos_neg'])
    datas_frame.set_index('compang_name', inplace=True)

    wi = countWeight_two(datas_frame, button_type)

    df_res = topsis(datas_frame, wi, 'topcis法')

    # 删除索引相同的值
    df_res = df_res.drop_duplicates('compang_name', keep='first')
    df_res.set_index('compang_name', inplace=True)

    # 将竞争力分数合并到上传数据后
    df_information = pd.DataFrame(pd.read_excel(uplaod_file))
    df_information.rename(columns={df_information.columns[0]: 'compang_name'}, inplace=True)
    df_information = df_information.drop_duplicates('compang_name', keep='first')
    df_information.set_index('compang_name', inplace=True)

    df_res = pd.concat([df_information, df_res], axis=1)
    df_res.sort_values(by="topcis法", inplace=True, ascending=False)
    for info in zip(df_res.index, df_res.iloc):
        if models.Rank.objects.filter(Q(type=button_type) & Q(name=info[0])).exists():
            models.Rank.objects.filter(Q(type=button_type) & Q(name=info[0])).update(score=info[1]['topcis法'])
            df_res = df_res.drop(index=info[0])

    print('-----新插入的数据信息-----')
    print(df_res)

    if df_res.index.empty:
        print('没有发现新的插入数据')

    else:
        df_res.to_excel(uplaod_file_score)
        print('对文档竞争力分析结合')
