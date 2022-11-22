import json
from pyecharts import options as opts
from pyecharts.charts import Map,Geo, Tab
from pyecharts.faker import Faker
import os
from pyecharts.globals import ChartType,ThemeType
import pandas
from pyecharts.charts import Bar, Grid, Line, Liquid, Page, Pie

def read_excel(filename):
    '''

    :param filename
    :return: datas
             colunm_name
    '''
    datas = pandas.read_excel(filename)
    column_name = datas.columns

    return datas,column_name

def ShowManageCityData(datas,AreaType,Type,location,title):
    grid = Grid(init_opts=opts.InitOpts(theme=ThemeType.ROMA, width='1600px'))
    use_data = datas[['Name','Num']][datas.AreaType==AreaType][datas.Type==Type].values.tolist()
    # print(use_data)
    c = (
        Map()
        .add(
            "CompanyNum",
            use_data,
            location,
            zoom=1.2
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(title=title), visualmap_opts=opts.VisualMapOpts()
        )
    )
    grid.add(c,grid_opts=opts.GridOpts(pos_right="25%"))
    return grid

def ShowPie(datas,AreaType,Type,location,title):
    city_county = {'深圳': ['盐田区', '坪山区', '罗湖区', '福田区', '南山区', '龙岗区', '龙华区', '宝安区', '光明区'],
     '广州': ['花都区', '黄埔区', '海珠区', '从化区', '番禺区', '南沙区', '荔湾区', '越秀区', '天河区', '白云区', '增城区'], '珠海': ['斗门区', '香洲区', '金湾区'],
     '佛山': ['高明区', '禅城区', '南海区', '顺德区', '三水区'], '东莞': ['-'], '江门': ['江海区', '蓬江区', '新会区', '恩平市', '鹤山市', '开平市', '台山市'],
     '汕头': ['龙湖区', '潮南区', '金平区', '潮阳区', '濠江区', '澄海区'], '惠州': ['惠城区', '博罗县', '惠东县', '惠阳区'], '中山': ['-'],
     '茂名': ['电白区', '高州市', '茂南区', '化州市'], '清远': ['连山壮族瑶族自治县', '清城区', '佛冈县', '英德市'],
     '肇庆': ['鼎湖区', '高要区', '怀集县', '广宁县', '端州区', '四会市'], '阳江': ['阳东区', '江城区'], '河源': ['源城区', '紫金县'], '云浮': ['云城区', '新兴县'],
     '湛江': ['雷州市', '遂溪县', '赤坎区', '坡头区', '霞山区'], '揭阳': ['揭东区', '榕城区', '惠来县', '普宁市'], '汕尾': ['海丰县', '城区', '陆丰市'],
     '韶关': ['曲江区', '武江区', '浈江区', '乳源瑶族自治县'], '梅州': ['梅县区', '梅江区', '平远县', '兴宁市', '五华县'], '潮州': ['湘桥区', '潮安区', '饶平县']}

    use_data = datas[['Name','Num']][datas.AreaType==AreaType][datas.Type==Type].values.tolist()
    print(location)
    if AreaType != 'city':
        county_showed = city_county[location]
        print(use_data)
        use_data = [i for i in use_data if i[0] in county_showed]
        print(use_data)
    if location == '东莞' or location == '中山':
        use_data = [i for i in use_data if i[0][:-1] == location]

    if len(use_data) == 0:
        use_data = [['None',1]]
    pie = Pie(init_opts=opts.InitOpts(theme='light',
                                      width='1000px',
                                      height='1000px'))
    pie.add("", use_data)
    #设置标题
    pie.set_global_opts(title_opts=opts.TitleOpts(title=title),
                        #设置图例位置
                       legend_opts=opts.LegendOpts(type_="scroll", pos_left="90%", orient="vertical"),)
    pie.set_series_opts(
        # 自定义数据标签
        label_opts=opts.LabelOpts(position='top',
                                  color='blue',
                                  font_family='Arial',
                                  font_size=12,
                                  font_style='italic',
                                  interval=1,
                                  formatter='{b}:{d}%'
                                  )
    )

    # c = (
    #     Map()
    #     .add(
    #         "CompanyNum",
    #         use_data,
    #         location,
    #         zoom=1.2
    #     )
    #     .set_global_opts(
    #         title_opts=opts.TitleOpts(title=title), visualmap_opts=opts.VisualMapOpts()
    #     )
    # )
    # grid = (
    #     Grid(init_opts=opts.InitOpts(width="1200px", height="1200px"))
    #     .add(pie, grid_opts=opts.GridOpts(pos_left="75%", pos_top="50%", is_show=True))
    #     .add(c,grid_opts=opts.GridOpts(pos_left="10%",pos_top="80%"))
    # )
    return pie

def province(datas):
    tab = Tab()
    tab.add(ShowManageCityData(datas,'city','manage','广东','广东省工业软件信息管理类'), "广东省工业软件信息管理类-地图可视化-地图")
    tab.add(ShowManageCityData(datas,'city','control','广东','广东省工业软件生产控制类'), "广东省工业软件生产控制类-地图")
    tab.add(ShowManageCityData(datas,'city','embedded','广东','广东省工业软件嵌入式'), "广东省工业软件嵌入式-地图")
    tab.add(ShowManageCityData(datas,'city','product','广东','广东省工业软件产品研发类'), "广东省工业软件产品研发类-地图")
    tab.add(ShowPie(datas,'city','manage','广东','广东省工业软件信息管理类'), "广东省工业软件信息管理类-饼图")
    tab.add(ShowPie(datas,'city','control','广东','广东省工业软件生产控制类'), "广东省工业软件生产控制类-饼图")
    tab.add(ShowPie(datas,'city','embedded','广东','广东省工业软件嵌入式'), "广东省工业软件嵌入式-饼图")
    tab.add(ShowPie(datas,'city','product','广东','广东省工业软件产品研发类'), "广东省工业软件产品研发类-饼图")
    tab.render("/root/industry_software/templates/广东.html")

    with open("/root/industry_software/templates/广东.html") as f:
        html = f.read()
        html = html.replace('<div class="tab">','<div class="tab">\n<button onclick="window.location.href=\'vi\'">返回首页</button>')
    with open("/root/industry_software/templates/广东.html",'w') as f:
        f.write(html)

def city(datas):
    citys = ['深圳', '广州', '珠海', '佛山', '东莞', '江门', '汕头', '惠州', '中山', '茂名', '清远', '肇庆', '阳江', '河源', '云浮', '湛江', '揭阳', '汕尾', '韶关', '梅州', '潮州']
    for city in citys:
        tab = Tab()
        if city == '东莞' or city == '中山':
            tab.add(ShowManageCityData(datas, 'city', 'manage', city, city + '市工业软件信息管理类'), city + "市工业软件信息管理类-地图")
            tab.add(ShowManageCityData(datas, 'city', 'control', city, city + '市工业软件生产控制类'), city + "市工业软件生产控制类-地图")
            tab.add(ShowManageCityData(datas, 'city', 'embedded', city, city + '市工业软件嵌入式'), city + "市工业软件嵌入式-地图")
            tab.add(ShowManageCityData(datas, 'city', 'product', city, city + '市工业软件产品研发类'), city + "市工业软件产品研发类-地图")
            tab.add(ShowPie(datas, 'city', 'manage', city, city + '市工业软件信息管理类'), city + "市工业软件信息管理类-饼图")
            tab.add(ShowPie(datas, 'city', 'control', city, city + '市工业软件生产控制类'), city + "市工业软件生产控制类-饼图")
            tab.add(ShowPie(datas, 'city', 'embedded', city, city + '市工业软件嵌入式'), city + "市工业软件嵌入式-饼图")
            tab.add(ShowPie(datas, 'city', 'product', city, city + '市工业软件产品研发类'), city + "市工业软件产品研发类-饼图")
        else:
            tab.add(ShowManageCityData(datas, 'county', 'manage', city, city+'市工业软件信息管理类'), city+"市工业软件信息管理类-地图")
            tab.add(ShowManageCityData(datas, 'county', 'control', city, city+'市工业软件生产控制类'), city+"市工业软件生产控制类-地图")
            tab.add(ShowManageCityData(datas, 'county', 'embedded', city, city+'市工业软件嵌入式'), city+"市工业软件嵌入式-地图")
            tab.add(ShowManageCityData(datas, 'county', 'product', city, city+'市工业软件产品研发类'), city+"市工业软件产品研发类-地图")
            tab.add(ShowPie(datas, 'county', 'manage', city, city + '市工业软件信息管理类'), city + "市工业软件信息管理类-饼图")
            tab.add(ShowPie(datas, 'county', 'control', city, city + '市工业软件生产控制类'), city + "市工业软件生产控制类-饼图")
            tab.add(ShowPie(datas, 'county', 'embedded', city, city + '市工业软件嵌入式'), city + "市工业软件嵌入式-饼图")
            tab.add(ShowPie(datas, 'county', 'product', city, city + '市工业软件产品研发类'), city + "市工业软件产品研发类-饼图")
        tab.render("/root/industry_software/templates/"+city+".html")

        with open("/root/industry_software/templates/"+city+".html") as f:
            html = f.read()
            html = html.replace('<div class="tab">',
                                '<div class="tab">\n<button onclick="window.location.href=\'vi\'">返回首页</button>')
        with open("/root/industry_software/templates/"+city+".html", 'w') as f:
            f.write(html)

def main(datas):
    province(datas)
    city(datas)

if __name__ == '__main__':
    # Load Data
    datas,column_name = read_excel('/root/industry_software/industry_software/dataset/Area_data.xlsx')
    main(datas)
