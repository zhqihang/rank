from django.contrib import admin
from myapp import models

# Register your models here.
admin.site.register(models.Rank)
admin.site.register(models.Company)
admin.site.register(models.Products)

# admin.site.register(models.Rank_3)
