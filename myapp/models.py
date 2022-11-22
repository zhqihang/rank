from django.db import models

# Create your models here.
class Company(models.Model):
    name = models.CharField(verbose_name="公司名称",max_length=64,unique=True,primary_key=True)
    product_num = models.IntegerField(verbose_name="产品总数",default=0)
    fz_product = models.IntegerField(verbose_name="工业软件仿真设计产品个数",default=0)
    qr_product = models.IntegerField(verbose_name="工业软件嵌入式系统产品个数",default=0)
    kz_product = models.IntegerField(verbose_name="工业软件生产调度和过程控制产品个数",default=0)
    jy_product = models.IntegerField(verbose_name="工业软件经营信息管理产品个数",default=0)
    pt_product = models.IntegerField(verbose_name="工业软件平台与系统产品个数",default=0)
    assets = models.FloatField(default=0)
    income = models.FloatField(default=0)
    yield_rate = models.FloatField(default=0)
    total_content = models.FloatField(default=0)
    capital = models.FloatField(default=0)
    range = models.CharField(max_length=1000,default=None)
    Introduction = models.CharField(max_length=500,default=None)
    pos_neg = models.FloatField(default=0)

class Rank(models.Model):
    rank_id = models.IntegerField(primary_key=True)
    name =  models.CharField(max_length=50)
    score = models.FloatField()
    type = models.CharField(max_length=50)
    expert_score = models.FloatField(default=0)

# 创建产品表
class Products(models.Model):
    pro_id = models.IntegerField(primary_key=True)
    pro_company = models.CharField(verbose_name="所属公司",max_length=50)
    # 定义产品类型约束，可以使用obj.get_pro_type_display()获取“***”对应内容
    pro_type_choices = (
        (1,"工业软件仿真设计产品"),
        (2,"工业软件嵌入式系统产品"),
        (3,"工业软件生产调度和过程控制产品"),
        (4,"工业软件经营信息管理产品"),
        (5,"工业软件平台与系统产品")
    )
    pro_type = models.SmallIntegerField(verbose_name="产品类型",choices=pro_type_choices,null=True)
    pro_detail = models.CharField(verbose_name="产品描述",max_length=1000)

class Expert(models.Model):
    expert_id = models.IntegerField(primary_key=True)
    account = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    weight = models.FloatField()

# class Rank_3(models.Model):
#     rank_id = models.IntegerField(primary_key=True)
#     name = models.CharField(max_length=50)
#     assets = models.CharField(max_length=50)
#     income = models.CharField(max_length=50)
#     yield_rate = models.CharField(max_length=50)
#     total_content = models.CharField(max_length=50)
#     capital = models.CharField(max_length=50)
#     product = models.CharField(max_length=50)
#     range = models.CharField(max_length=1000)
#     Introduction = models.CharField(max_length=500)
#     score = models.CharField(max_length=50)
#     type = models.CharField(max_length=50)
