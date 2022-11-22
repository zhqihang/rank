# coding = utf-8

import os
import pandas as pd

Folder_Path = "four"
# 获取当前路径
cwd = os.getcwd()
# 修改当前工作目录
print('当前工作目录: '+cwd)

# 将该文件夹下的所有文件名存入一个列表
file_list = os.listdir(cwd+"/"+Folder_Path)
print(file_list)
data_all = []
for i in range(len(file_list)):
    df_excel = pd.read_excel(cwd+"/"+Folder_Path+"/"+file_list[i])
    df_excel["类型"] = file_list[i][:-5]
    data_all.append(df_excel)
df_all = pd.concat(data_all, axis=0)
df_all.to_excel(cwd+"/"+"data.xlsx", sheet_name="sheet1", header= None, index=False)