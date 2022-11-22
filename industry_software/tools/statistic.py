import numpy as np
import pandas as pd
import re
import json
import jieba
from collections import Counter

# jieba词频统计
# information_filer = '/data/zhanghongbin/industry_software/industry_software/dataset/four/广东省工业软件产品研发类.xls'
#
# cut_words=""
# df_information = pd.read_excel(information_filer)
# for index, row in df_information.iterrows():
#     row.values[-1] = row.values[-1].rstrip("\n")
#     row.values[-1] = re.sub("[A-Za-z0-9\：\·\，\。\“\”\；\(\)\;\、\（\）\'\,]", "", row.values[-1])
#     seg_list = jieba.cut(row.values[-1], cut_all=True)
#     cut_words += (" ".join(seg_list))
#
# all_words=cut_words.split()
# print(all_words)
# c=Counter()
# d=Counter()
# e=Counter()
# f=Counter()
# for x in all_words:
#     if len(x)>1 and x != '\r\n':
#         c[x] += 1
#     if len(x)>2 and x != '\r\n':
#         d[x] += 1
#     if len(x)>3 and x != '\r\n':
#         e[x] += 1
#     if len(x)>4 and x != '\r\n':
#         f[x] += 1
#
# print('\n>1词频统计结果：')
# for (k,v) in c.most_common(50):# 输出词频最高的前两个词
#     print("%s:%d"%(k,v))
#
# print('\n>2词频统计结果：')
# for (k,v) in d.most_common(50):
#     print("%s:%d"%(k,v))
#
# print('\n>3词频统计结果：')
# for (k,v) in e.most_common(100):
#     print("%s:%d"%(k,v))
#
# print('\n>4词频统计结果：')
# for (k,v) in f.most_common(100):
#     print("%s:%d"%(k,v))

def get_range_intruduction(text):
    print('初始文本_' + text)
    # 经过数据处理后的经验范围
    range = []
    text = text.rstrip("\n")
    # 删除括号内的信息
    text = re.sub('\(依法须经批准的项目，经相关部门批准后方可开展经营活动\)|'
                  '\(法律、行政法规、国务院决定规定在登记前须经批准的项目除外\)|'
                  '\（依法须经批准的项目，经相关部门批准后方可开展经营活动）|'
                  '\（法律、行政法规、国务院决定规定在登记前须经批准的项目除外\）|'
                  '\（不含限制项目）|'
                  '\（不含限制项目\）', '', text)
    text = text.replace("〓", "")
    text = text.replace(" ", "")
    # 根据特殊符号分割
    text_list = re.split('！|；|;|。|\.|,|，', text)
    # list中将空字符串移除
    while '' in text_list:
        text_list.remove('')
    print(text_list)

    split_first = ['、', '：']
    split_first_ = ['、', ':']
    split_second = ['：', ':']
    start_first = ['一般项目', '一般经营项目是', '一般']
    start_second = ['许可项目', '许可经营项目是', '许可']
    # end_first = ['研发', '设计', '开发', '研究', '生产', '加工', '销售', '制造', '安装']
    for row in text_list:
        print(row)
        # 根据、和：或:进行组合
        if all(key in row for key in split_first) or all(key in row for key in split_first_):
            if split_first[1] in row:
                symbol = split_first[1]
            else:
                symbol = split_first_[1]
            row_list = re.split(symbol, row)
            if any(key in row_list[0] for key in start_first) or any(key in row_list[0] for key in start_second):
                range.append(row_list[1])
            # elif any(key in row_list[0] for key in end_first):
            #     # 添加到列表
            #     range.append(row)
            else:
                # 添加到列表
                range.append(row)
        # 根据:进行
        elif any(key in row for key in split_second):
            if split_second[0] in row:
                symbol = split_second[0]
            else:
                symbol = split_second[1]
            row_list = re.split(symbol, row)
            if any(key in row_list[0] for key in start_first) or any(key in row_list[0] for key in start_second):
                if row_list[1] is not '':
                    range.append(row_list[1])
            elif row_list[1] is not '':
                range.append(row_list[0])
                range.append(row_list[1])
        # # 根据、:进行
        # elif '、' in row:
        #     if any(key in row for key in end_first):
        #         # 添加到列表
        #         range.append(row)
        else:
            range.append(row)
    print(range)
    return range

# 工业软件研发设计类
research_keywords_one = ['CAD', '辅助设计']
research_keywords_two = ['CAE', '辅助分析']
research_keywords_three = ['CAM', '辅助制造']
research_keywords_four = ['PDM', '产品数据管理', '数据管理', 'cPDM']
research_keywords_five = ['PLM', '产品生命周期管理', '产品周期', '周期管理', '生命周期', '产品生命']
research_keywords_six = ['EDA', 'EDN', '电子设计自动化', '电子设计', '设计自动', '软件工具']
research_keywords_seven = ['CAPP', '辅助工艺规划', '辅助工艺', '工艺规划', '辅助规划']
research_keywords_eight = ['CIM', '半导体CIM']
research_keywords_nigh = ['SCA', '组成分析', '成本分析']
research_keywords_ten = ['MBSE', '基于模型的系统工程', '基于模型系统', '基于模型工程']
research_keywords_eleven = ['SaaS', '软件服务', '数字化软件', '全流程软件', '工业一体化', '数字装备', '数字化装备', '一体化软件',
                          '一体化装备', '工业操作系统', '自动化软件']
research_keywords = [research_keywords_one, research_keywords_two, research_keywords_three, research_keywords_four,
                     research_keywords_five, research_keywords_six, research_keywords_seven, research_keywords_eight,
                     research_keywords_nigh, research_keywords_ten, research_keywords_eleven]

# CAD 功能
research_key_1_1 = ['计算机', '工程', '研发']
research_key_1_2 = ['工业', '工程', '设计']

# EDA EDN 功能
research_key_2_1 = ['电子自动', '研发']
research_key_2_2 = ['芯片', '设计']
research_key_2_3 = ['电路', '研发']

# CAE CAM 功能
research_key_3_1 = ['工业', '仿真', '研发']
research_key_3_2 = ['工业', '仿真', '设计']
research_key_3_3 = ['工业', '仿真', '分析']

research_key_4_1 = ['工业', '互联网', '研发']
research_key_4_2 = ['工业', '互联网', '设计']

research_name_1_1 = ['工业', '软件', '研发']
research_name_1_2 = ['工业', '软件', '设计']

research_key_one_2 = [research_key_1_1, research_key_1_2]
research_key_two_3 = [research_key_2_1, research_key_2_2, research_key_2_3]
research_key_three_3 = [research_key_3_1, research_key_3_2, research_key_3_3]
research_key_four_2 = [research_key_4_1, research_key_4_2]
research_name_one_2 = [research_name_1_1, research_name_1_2]

research_key = [research_key_one_2, research_key_two_3, research_key_three_3, research_key_four_2, research_name_one_2]

# 工业软件嵌入式类
embedding_keywords_one = ['嵌入工业装备软件', '嵌入工业装备', '嵌入工业', '嵌入工业软件', '嵌入装备软件']
embedding_keywords_two = ['PLC', '可编程逻辑控制器', '编程逻辑', '编程控制', '数字逻辑控制', '编程存储']
embedding_keywords_three = ['嵌入式系统']
embedding_keywords_four = ['嵌入式电子', '嵌入式设备']
embedding_keywords_five = ['ICT', '信息通信', '通信信息', '信息与通信', '通信与信息', '网络通信']
embedding_keywords_six = ['芯片', '微电子']
embedding_keywords = [embedding_keywords_one, embedding_keywords_two, embedding_keywords_three,
                      embedding_keywords_four, embedding_keywords_five, embedding_keywords_six]

# 嵌入式系统 功能
embedding_key_1_1 = ['工业', '设备', '传感器']
embedding_key_1_2 = ['工业', '设备', '集成电路']

# 电子
embedding_key_3_1 = ['工业','电子自动', '电子设计']

embedding_name_1_1 = ['工业', '软件', '嵌入式']

embedding_key_one_2 = [embedding_key_1_1, embedding_key_1_2]
embedding_key_two_1 = [embedding_key_3_1]
embedding_name_one_1 = [embedding_name_1_1]

embedding_key = [embedding_key_one_2, embedding_key_two_1, embedding_name_one_1]

# 工业软件生产控制类
control_keywords_one = ['MES', '制造执行系统', '制造执行', '执行系统', '能源管理软件', '能源软件']
control_keywords_two = ['APS', '高级计划持产系统', '高级计划', '计划持产', '持产系统']
control_keywords_three = ['SCADA', '数据采集与监视控制系统', '数据采集', '监视控制', '组态软件', '组态监控']
control_keywords_four = ['DCS', '集散控制系统', '集散控制']
control_keywords_five = ['MOM', '制造运营管理', '制造运营', '制造管理', '运营管理']
control_keywords_six = ['APC', '先进过程控制', '先进过程', '过程控制', '先进控制']
control_keywords_seven = ['QMS', '质量管理信息系统', '质量管理', '质量信息', '质量系统', '管理信息']
control_keywords_eight = ['WMS', '仓储管理系统', '仓储管理']
control_keywords = [control_keywords_one, control_keywords_two, control_keywords_three, control_keywords_four,
                    control_keywords_five, control_keywords_six, control_keywords_seven, control_keywords_eight]

# MES 功能
control_key_1_1 = ['工业', '生产信息', '执行生产']
control_key_1_2 = ['工业', '生产信息', '执行计划']
control_key_1_3 = ['工业', '生产信息', '质量问题']
control_key_1_4 = ['工业', '生产信息', '生产效率']
control_key_1_5 = ['工业', '生产信息', '管理效率']

# DCS 功能 SCADA 功能
control_key_2_1 = ['工业', '自动控制', '操作管理']
control_key_2_2 = ['工业', '自动控制', '分散控制']
control_key_2_3 = ['工业', '自动控制', '自治']

# 生产控制 功能
control_key_4_1 = ['工业', '软件', '生产调度']
control_key_4_2 = ['工业', '软件', '能耗管理']
control_key_4_3 = ['工业', '软件', '过程执行']
control_name_1_1 = ['工业', '软件', '生产控制']
control_name_1_2 = ['工业', '软件', '控制生产']

control_key_one_5 = [control_key_1_1, control_key_1_2, control_key_1_3, control_key_1_4, control_key_1_5]
control_key_two_3 = [control_key_2_1, control_key_2_2, control_key_2_3]
control_name_one_1 = [control_name_1_1, control_name_1_2, control_key_4_1, control_key_4_2, control_key_4_3]

control_key = [control_key_one_5, control_key_two_3, control_name_one_1]

# 工业软件信息管理类
manage_keywords_one = ['ERP', '企业资源计划', '企业资源', '资源计划']
manage_keywords_two = ['CRM', '客户关系管理', '客户关系', '关系管理', '营销管理']
manage_keywords_three = ['SCM', '供应链管理']
manage_keywords_four = ['HRM', 'HCM', '人力资源管理', '人力资源', '资源管理']
manage_keywords_five = ['EAM', '企业资产管理', '企业资产', '资产管理']
manage_keywords_six = ['FM', '财务管理']
manage_keywords_seven = ['BI', '商业智能']
manage_keywords_eight = ['TMS', '运输管理']
manage_keywords_nigh = ['MRO', '运维综合保障管理系统', '运维综合', '运维保障', '综合保障', '保障管理', '运维管理']
manage_keywords_ten = ['SRM', '供应商关系管理', '供应商管理']
manage_keywords_eleven = ['DMS', '经销商管理']
manage_keywords_twelve = ['LIMS', '实验室信息管理系统', '实验室信息']
manage_keywords_twelve = ['OA', '办公协同']
manage_keywords = [manage_keywords_one, manage_keywords_two, manage_keywords_three, manage_keywords_four,
                   manage_keywords_five, manage_keywords_six, manage_keywords_seven, manage_keywords_eight,
                   manage_keywords_nigh, manage_keywords_ten, manage_keywords_eleven, manage_keywords_twelve]

# EPR 功能 CRM 功能
manage_key_1_1 = ['工业', '信息化', '核心系统']
manage_key_1_2 = ['工业', '系统化', '管理平台']
manage_key_1_3 = ['工业', '一体化', '管理软件']
manage_key_1_4 = ['工业', '信息化', '经营流程']

# CRM 功能
manage_key_2_2 = ['工业', '客户资源', '管理软件']

# SCM 功能
manage_key_3_1 = ['工业', '供应链', '执行']
manage_key_3_2 = ['工业', '供应链', '计划']
manage_key_3_3 = ['工业', '供应链', '规划']

manage_name_1_1 = ['工业', '软件', '信息管理']
manage_name_1_2 = ['工业', '软件', '管理信息']

manage_key_one_4 = [manage_key_1_1, manage_key_1_2, manage_key_1_3, manage_key_1_4]
manage_key_two_2 = [manage_key_2_2]
manage_key_three_3 = [manage_key_3_1, manage_key_3_2, manage_key_3_3]
manage_name_one_1 = [manage_key_one_4, manage_key_two_2, manage_name_1_1, manage_name_1_2]

manage_key = [manage_name_one_1]

positive = ['智能', '智慧', '工业', '软件', '物联网', '云平台', '控制器', '边缘']
positive_2 = ['工业自动化', '工业机器人', '工业智能', '工业相机', '工业软件', '工业控制', '自动化制造',
              '数控', '自动化测量', '能源电子', '工业过程控制', '数字控制', '信号自动控制', '系统集成',
              '集成电路', '工业读码器', '工业自动控制', '仿真', ]
negtive = ['批发', '广告', '货物', '房地产', '电子商务', '食品', '生物', '日用', '餐饮', '服装', '体育',
           '娱乐', '休闲', '酒店', '投资', '营销策划', '景观', '园林', '房屋', '装饰', '装修', '市政',
           '咨询', '动漫', '新闻', '电影', '土地', '形象', '展台', '美术', '展览', '平面', '会议', '灯饰',
           '招标', '代理', '环保', '旅游', '教育']

def iterator(num, info, type_keywords):
    for each in info:
        for key_list in type_keywords:
            flag = False
            for key in key_list:
                if key in each:
                    print('---'+key)
                    flag = True
            if flag:
                num += 10000
    return num

def iterator_two(num, info, type_key):
    one = 0
    two = 0
    three = 0
    for each in info:
        for key_list in type_key:
            key_flag = 0
            if len(key_list) == 1:
                for a in key_list[0]:
                    if a in each:
                        key_flag += 1
            if len(key_list) == 2:
                for a, b in zip(key_list[0], key_list[1]):
                    if (a in each) or (b in each):
                        key_flag += 1
            elif len(key_list) == 3:
                for a, b, c in zip(key_list[0], key_list[1], key_list[2]):
                    if (a in each) or (b in each) or (c in each):
                        key_flag += 1
            elif len(key_list) == 4:
                for a, b, c, d in zip(key_list[0], key_list[1], key_list[2], key_list[3]):
                    if (a in each) or (b in each) or (c in each) or (d in each):
                        key_flag += 1
            elif len(key_list) == 5:
                for a, b, c, d, e in zip(key_list[0], key_list[1], key_list[2], key_list[3], key_list[4]):
                    if (a in each) or (b in each) or (c in each) or (d in each) or (e in each):
                        key_flag += 1
            elif len(key_list) == 6:
                for a, b, c, d, e, f in zip(key_list[0], key_list[1], key_list[2], key_list[3], key_list[4], key_list[5]):
                    if (a in each) or (b in each) or (c in each) or (d in each) or (e in each) or (f in each):
                        key_flag += 1
            elif len(key_list) == 7:
                for a, b, c, d, e, f, g in zip(key_list[0], key_list[1], key_list[2], key_list[3], key_list[4], key_list[5], key_list[6]):
                    if (a in each) or (b in each) or (c in each) or (d in each) or (e in each) or (f in each) or (g in each):
                        key_flag += 1
            elif len(key_list) == 8:
                for a, b, c, d, e, f, g, h in zip(key_list[0], key_list[1], key_list[2], key_list[3], key_list[4], key_list[5], key_list[6], key_list[7]):
                    if (a in each) or (b in each) or (c in each) or (d in each) or (e in each) or (f in each) or (g in each) or (h in each):
                        key_flag += 1
            if key_flag == 1:
                one += 1
            if key_flag == 2:
                num += 1
                two += 1
            elif key_flag == 3:
                num += 1000
                three += 1
    print('1---' + str(one))
    print('2---' + str(two))
    print('3---' + str(three))
    return num

def pos_neg_iterator(number, info, type_pos, type_pos_two, type_neg):
    for each in info:
        pos_tag = 0
        for pos in type_pos:
            if pos in each:
                print('pos---'+pos)
                pos_tag += 1
        number += (pos_tag * 1)
        pos_tag_two = 0
        for pos_two in type_pos_two:
            if pos_two in each:
                print('pos_two---' + pos_two)
                pos_tag_two += 1
        number += (pos_tag_two * 10)
        neg_tag = 0
        for neg in type_neg:
            if neg in each:
                print('neg------' + neg)
                neg_tag += 1
        number -= (neg_tag * 3)
    return number

def range_introduction_iterrow(df_range_introduction, button_type):
    for index, row in df_range_introduction.iterrows():
        # 经过预处理，将范围根据符号划分成多个句子
        range = get_range_intruduction(row.values[0])
        # 经过预处理，将范围和简介根据符号划分成多个句子
        introduction = get_range_intruduction(row.values[1])
        if button_type == '工业软件研发':
            # 根据范围 或 简介 累加出现关键词的次数
            key_num = 0
            key_num_two = 0
            # 分数占比比例
            # 用research_keywords词来匹配经营范围、公司简介, 103条数据中有统计数分别为: 1 5 2
            key_num = iterator(key_num, range, research_keywords)
            key_num = iterator(key_num, introduction, research_keywords)
            # 用专业词描述+类型名称来匹配经营范围、公司简介
            key_num = iterator_two(key_num, range, research_key)
            key_num = iterator_two(key_num, introduction, research_key)
            row.values[0] = key_num
            # 词频+启发式筛选负向词进行统计分别为:
            key_num_two = pos_neg_iterator(key_num_two, range, positive, positive_2, negtive)
            key_num_two = pos_neg_iterator(key_num_two, introduction, positive, positive_2, negtive)
            row.values[1] = key_num_two
        elif button_type == '工业软件嵌入式':
            key_num = 0
            key_num_two = 0
            # 用embedding_keywords词来匹配经营范围、公司简介, 16条数据中有统计数分别为: 3 1 1 1 1 2
            key_num = iterator(key_num, range, embedding_keywords)
            key_num = iterator(key_num, introduction, embedding_keywords)
            # 用专业词描述+类型名称来匹配经营范围、公司简介
            key_num = iterator_two(key_num, range, embedding_key)
            key_num = iterator_two(key_num, introduction, embedding_key)
            row.values[0] = key_num
            # 词频+启发式筛选负向词进行统计分别为:
            key_num_two = pos_neg_iterator(key_num_two, range, positive, positive_2, negtive)
            key_num_two = pos_neg_iterator(key_num_two, introduction, positive, positive_2, negtive)
            row.values[1] = key_num_two
        elif button_type == '工业软件生产控制':
            key_num = 0
            key_num_two = 0
            statistic_num = len(control_key)
            # 用embedding_keywords词来匹配经营范围、公司简介, 37条数据中有统计数分别为: 1 1 1 1 1 1
            key_num = iterator(key_num, range, control_keywords)
            key_num = iterator(key_num, introduction, control_keywords)
            # 用专业词描述+类型名称来匹配经营范围、公司简介
            key_num = iterator_two(key_num, range, control_key)
            key_num = iterator_two(key_num, introduction, control_key)
            row.values[0] = key_num
            # 词频+启发式筛选负向词进行统计分别为:
            key_num_two = pos_neg_iterator(key_num_two, range, positive, positive_2, negtive)
            key_num_two = pos_neg_iterator(key_num_two, introduction, positive, positive_2, negtive)
            row.values[1] = key_num_two
        elif button_type == '工业软件信息管理':
            key_num = 0
            key_num_two = 0
            # 用manage_keywords词来匹配经营范围、公司简介, 41条数据中有统计数分别为: 1 1 1 3 1 2 1 2 1 3 1 1 1 1
            key_num = iterator(key_num, range, manage_keywords)
            key_num = iterator(key_num, introduction, manage_keywords)
            # 用专业词描述+类型名称来匹配经营范围、公司简介
            key_num = iterator_two(key_num, range, control_key)
            key_num = iterator_two(key_num, introduction, control_key)
            row.values[0] = key_num
            # 词频+启发式筛选负向词进行统计分别为:
            key_num_two = pos_neg_iterator(key_num_two, range, positive, positive_2, negtive)
            key_num_two = pos_neg_iterator(key_num_two, introduction, positive, positive_2, negtive)
            row.values[1] = key_num_two
        else:
            print('类型未知')

def input_button(button):
    information_filer = '/data/zhanghongbin/industry_software/industry_software/dataset/four/'+button+'.xlsx'

    df_information = pd.read_excel(information_filer)
    df_range_introduction = pd.DataFrame(df_information, columns=['compang_name', '经营范围', '简介'])
    df_range_introduction.set_index('compang_name', inplace=True)
    return df_range_introduction

# button = '工业软件研发'
# df_range_introduction = input_button(button)
# range_introduction_iterrow(df_range_introduction, button)

# df_range_introduction.rename(columns={'经营范围': '专业名词得分', '简介': '词频+启发式得分'}, inplace=True)
# df_range_introduction.sort_values(by="专业名词得分", inplace=True, ascending=False)
# print(df_range_introduction)
# print(df_range_introduction.head(60))
# print(df_range_introduction.tail(43))
# print(df_range_introduction.max())
# print(df_range_introduction.min())
