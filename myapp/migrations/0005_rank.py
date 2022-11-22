# Generated by Django 3.1.3 on 2022-06-09 08:43

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('myapp', '0004_delete_rank'),
    ]

    operations = [
        migrations.CreateModel(
            name='Rank',
            fields=[
                ('rank_id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('assets', models.FloatField()),
                ('income', models.FloatField()),
                ('yield_rate', models.FloatField()),
                ('total_content', models.FloatField()),
                ('capital', models.FloatField()),
                ('product', models.FloatField()),
                ('range', models.CharField(max_length=1000)),
                ('Introduction', models.CharField(max_length=500)),
                ('score', models.FloatField()),
                ('type', models.CharField(max_length=50)),
            ],
        ),
    ]
