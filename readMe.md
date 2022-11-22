##流程
工作站项目目录：/data/userData/wmb/test_sh/industry_software/ python运行环境：movie（需要conda activate movie）
运行网站，最好用命令行运行，先去到manage.py目录下
python manage.py runserver 222.200.105.87:8000（这里222.200.105.87是ip地址，可以改为localhost，也可以修改为127.0.0.1同样表达本地，也可以直接修改为本地ip地址，例如222.200.105.87； 而端口号根据计算机自己的开放的端口，例如7000,6000,8001）

1. urls.py匹配指定path地址。urls.py文件指定网址path对应规则
2. 指定地址跳转到function.py文件里，找到对应方法调用的HTML。function.py文件指定一系列方法，调用对应HTML文件。
  request方法里的form中包含网页请求内容，可以在这里对内容进行处理。
3. templates文件夹下包含一系列HTML文件，即页面展示效果。
4. function.py文件
  request.GET()可以获得form内容 例如 表单form提交过程中 用name来进行传参
  render可以传输一部分内容到HTML中，方法是字典。{'key' : value}。HTML文档使用{{ key }}展示内容。

## excel操作
./industry_software/industry_software/dataset/excel_to_excel.py
主要为4个excel表（./industry_software/industry_software/dataset/four）的各自添加一列表名，然后将这4个更新后的表合并到1个excel表中，【最终的data.xlsx没有列名】

## 数据库的信息简述
django自带sqlite3数据库，在数据库中生成Rank表的参考链接如下（本项目已经根据相应步骤建构好了Rank表，相似可看./industry_software/myapp/models.py） 可以看到有共有12个字段，第一个字段唯一ID识别码，插入时不需要输入，表自动生成
https://blog.csdn.net/weixin_44605462/article/details/90484429
为了更直观地查看数据表的数据，和对数据表进行对应的操作，在运行网站后，在网址后加/admin访问数据库信息 里面myapp下有Rank表（例如在网页输入 localhost:7000/admin） 账号：root 密码：root
对数据表进行添加操作可以参考（这里针对路径下的excel表进行插入操作） ./industry_software/industry_software/rank/excel_to_db.py 

## 功能要求
针对功能开发（网上搜索的出现views.py 等于 本项目的 funciton.py）：
1、人工导入数据上传问题
a.这个需要考虑上传数据是否重复问题，【针对两个字段进行判定，一个是./industry_software/myapp/models.py下的name（公司名）、一个是./industry_software/myapp/models.py下的type（主要产品类型）】
b.考虑要指定哪个类型（工业软件嵌入式、工业软件生产控制、工业软件信息管理、工业软件研发），在前端加入一个下拉菜单 或者 单选框来判断字段，数据表输入的demo参考./industry_software/industry_software/rank/excel_to_db.py，但那个插入没有判断是否重复，需要结合步骤a完成

2、下载按钮点击（这里要考虑两种情况，一种是没有关键词查询的下载，一种是有关键词搜索查询的下载。但不重要，先做出来再说），该按钮已经设置在rank.html的form表单中，作为一个提交按钮，其功能和查询差不多，不同的是需要在function.py的def rank(request)函数上追加查询数据下载excel的功能
具体参考：https://www.cnblogs.com/joker-cai/p/12031771.html ； https://blog.csdn.net/qq28129019/article/details/107763557 ； https://blog.csdn.net/xdf19941224/article/details/93626524 ； 









1、排行榜点击查询详情（这个需要考虑url传参问题）
具体参考：百度根据ID查询数据库中的信息，然后返回到前段进行展示

2、可视化分析（已经可以通过./industry_software/industry_software/tools/show_area_data.py生成各个市的区的静态html）但在urls.py、function.py和home.html还没配置完，只配置到东莞，还需要补充
目前是静态的（解释：这里是不需要更新的，因为我这个是总的统计，但是另外四个数据是只有几十条数据的，也就是说用户插入的企业，其实已经在总的里面了）