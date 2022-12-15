# -*- encoding: utf-8 -*-
'''
@File   ：main.py 
@Time   ：2021/7/15 17:22
@Author : zdc
'''
import pandas as pd
from sklearn.cluster import KMeans
import numpy as np
#应用肘部法则确定 kmeans方法中的k
from scipy.spatial.distance import cdist
import matplotlib.pyplot as plt
import json

def dataPreprocess(path1,path2):
    df1 = pd.read_excel(path1, sheet_name='Sheet1')
    df2 = pd.read_excel(path2, sheet_name='Sheet1')
    df3 = pd.merge(df2, df1, on='comName')
    columnName = ['comName', 'comAddress', 'comRunInfo', 'lng', 'lat', '工业仿真设计', '工业嵌入式', '工业生产控制', '工业经营管理', '工业平台与系统'
        , '总产品数']
    df3 = df3.reindex(columns=columnName)
    return df3
def getSpecialColumnsFromDf(df,index,values):
    if isinstance(index,str):
        df1 = df[df[index] == 1].loc[:, values]

        df1.index=range(0,len(df1))
        return df1
    else:
        raise Exception('index不为字符串类型')
def my_kMeans(k,dataX):
    kmeans = KMeans(n_clusters=k)
    kmeans.fit(dataX)
    labels=pd.DataFrame(kmeans.labels_,columns=['label'])
    return labels,kmeans.cluster_centers_

def my_concat(df1,df2):
    df=pd.concat([df1,df2],axis=1)
    return df

def to_jsonFile(path,id,df,df_cluster_centers_):
    dic={}
    dic['id']=id
    dic["cluster_center"]=[]
    df_cluster_centers_list=df_cluster_centers_.tolist()
    for item in df_cluster_centers_list:
        temp={}
        temp['lng']=item[0]
        temp['lat']=item[1]
        dic["cluster_center"].append(temp)
    dic["data"]=[]
    for index,row in df.iterrows():
        temp={}
        temp["lng"]=row['lng']
        temp["lat"]=row['lat']
        temp["label"]=row['label']
        dic["data"].append(temp)
    # print(dic)
    with open(path, "w", encoding='utf-8') as f:
        json.dump(dic, f, indent=2, sort_keys=True, ensure_ascii=False)
def toJsonFile(path,listData):
    dic = {}
    dic['data']=[]
    for item in listData:
        temp={}
        temp['name']=item['name']
        temp['explanation']=item['explanation']
        temp['cluster_centers']=[]
        for data in item['data'].tolist():
            tempData={}
            tempData['lng'] = data[0]
            tempData['lat'] = data[1]
            temp['cluster_centers'].append(tempData)
        dic['data'].append(temp)
    with open(path, "w", encoding='utf-8') as f:
        json.dump(dic, f, indent=2, sort_keys=True, ensure_ascii=False)

def swicthClusterCenter2dic(name,explanation,data):
    temp = {}
    temp['name'] = name
    temp['explanation'] = explanation
    temp['data'] = data
    return temp

def count(path,series,narray):
    dic={}
    dic["cluster_center"]=[]
    listOfNarray=narray.tolist()
    countNum=0
    for index,value in series.items():
        temp={}
        temp1={}
        temp["label"]=index
        temp["count"]=value
        #把聚类中心经纬度存入temp1中
        temp1['lng'] = listOfNarray[countNum][0]
        temp1['lat'] = listOfNarray[countNum][1]
        temp["center"]=temp1
        dic["cluster_center"].append(temp)
        countNum+=1
    with open(path, "w", encoding='utf-8') as f:
        json.dump(dic, f, indent=2, sort_keys=True, ensure_ascii=False)

if __name__ == '__main__':
    path1='file:./data/info_matrix_totalData(最终文件).xlsx'
    path2='file:./data/lngAndLatData_qccCom(最终).xlsx'
    df=dataPreprocess(path1,path2)
    #把数据筛选出来
    # df_list=[]
    df_simulation=getSpecialColumnsFromDf(df,'工业仿真设计',('comName','comAddress','comRunInfo','lng','lat'))
    df_embedded=getSpecialColumnsFromDf(df,'工业嵌入式',('comName','comAddress','comRunInfo','lng','lat'))
    df_control=getSpecialColumnsFromDf(df,'工业生产控制',('comName','comAddress','comRunInfo','lng','lat'))
    df_management=getSpecialColumnsFromDf(df,'工业经营管理',('comName','comAddress','comRunInfo','lng','lat'))
    df_systems=getSpecialColumnsFromDf(df,'工业平台与系统',('comName','comAddress','comRunInfo','lng','lat'))
    df_all2=getSpecialColumnsFromDf(df,'总产品数',('comName','comAddress','comRunInfo','lng','lat'))



    #进行聚类
    df_total_labels,df_total_cluster_centers_=my_kMeans(5, df.loc[:,('lng','lat')])
    df_simulation_labels,df_simulation_cluster_centers_=my_kMeans(4,df_simulation.loc[:,('lng','lat')])
    df_embedded_labels,df_embedded_cluster_centers_=my_kMeans(3,df_embedded.loc[:,('lng','lat')])
    df_control_labels,df_control_cluster_centers_=my_kMeans(5,df_control.loc[:,('lng','lat')])
    df_management_labels,df_management_cluster_centers_=my_kMeans(5,df_management.loc[:,('lng','lat')])
    df_systems_labels,df_systems_cluster_centers_=my_kMeans(4,df_systems.loc[:,('lng','lat')])
    df_all2_labels,df_all2_cluster_centers_=my_kMeans(5,df_all2.loc[:,('lng','lat')])

    #把标签合并到原来的df中
    df_total=my_concat(df,df_total_labels)
    df_simulation=my_concat(df_simulation,df_simulation_labels)
    df_embedded=my_concat(df_embedded,df_embedded_labels)
    df_control=my_concat(df_control,df_control_labels)
    df_management=my_concat(df_management,df_management_labels)
    df_systems=my_concat(df_systems,df_systems_labels)
    df_all2=my_concat(df_all2,df_all2_labels)

    #输出成文件
    to_jsonFile(r'./output/json/total.json', 'all', df_total, df_total_cluster_centers_)
    to_jsonFile(r'./output/json/simulation.json', 'simulation', df_simulation, df_simulation_cluster_centers_)
    to_jsonFile(r'./output/json/embedded.json', 'embedded', df_embedded,
                df_embedded_cluster_centers_)
    to_jsonFile(r'./output/json/control.json', 'control', df_control, df_control_cluster_centers_)
    to_jsonFile(r'./output/json/management.json', 'management', df_management, df_management_cluster_centers_)
    to_jsonFile(r'./output/json/systems.json', 'systems', df_systems, df_systems_cluster_centers_)
    to_jsonFile(r'./output/json/all2.json', 'all2', df_all2, df_all2_cluster_centers_)

    # 把所有的聚类中心放在list中
    centerList = []
    centerList.append(swicthClusterCenter2dic('simulation', '涉及工业仿真设计的企业的聚类中心', df_simulation_cluster_centers_))
    centerList.append(swicthClusterCenter2dic('embedded', '涉及工业嵌入式的企业的聚类中心', df_embedded_cluster_centers_))
    centerList.append(swicthClusterCenter2dic('control', '涉及工业生产控制的企业的聚类中心', df_control_cluster_centers_))
    centerList.append(swicthClusterCenter2dic('management', '涉及工业经营管理的企业的聚类中心', df_management_cluster_centers_))
    centerList.append(swicthClusterCenter2dic('systems', '涉及工业平台与系统的企业的聚类中心', df_systems_cluster_centers_))
    centerList.append(swicthClusterCenter2dic('all2', '涉及工业的企业的聚类中心', df_all2_cluster_centers_))
    toJsonFile(r'./output/json/cluster_centers.json', centerList)
    # 统计标签
    count(r"./output/count/df_totalCount.json", df_total['label'].value_counts().sort_index(), df_total_cluster_centers_)
    count(r"./output/count/df_simulationCount.json", df_simulation['label'].value_counts().sort_index(), df_simulation_cluster_centers_)
    count(r"./output/count/df_embeddedCount.json", df_embedded['label'].value_counts().sort_index(),
          df_embedded_cluster_centers_)
    count(r"./output/count/df_controlCount.json", df_control['label'].value_counts().sort_index(),
          df_control_cluster_centers_)
    count(r"./output/count/df_managementCount.json", df_management['label'].value_counts().sort_index(),
          df_management_cluster_centers_)
    count(r"./output/count/df_systemsCount.json", df_systems['label'].value_counts().sort_index(),
          df_systems_cluster_centers_)
    count(r"./output/count/df_all2Count.json", df_all2['label'].value_counts().sort_index(), df_all2_cluster_centers_)



