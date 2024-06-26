# Generated by Django 3.1.3 on 2022-06-09 09:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0008_rank_2'),
    ]

    operations = [
        migrations.CreateModel(
            name='Rank_3',
            fields=[
                ('rank_id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('assets', models.CharField(max_length=50)),
                ('income', models.CharField(max_length=50)),
                ('yield_rate', models.CharField(max_length=50)),
                ('total_content', models.CharField(max_length=50)),
                ('capital', models.CharField(max_length=50)),
                ('product', models.CharField(max_length=50)),
                ('range', models.CharField(max_length=1000)),
                ('Introduction', models.CharField(max_length=500)),
                ('score', models.CharField(max_length=50)),
                ('type', models.CharField(max_length=50)),
            ],
        ),
    ]
