# Generated by Django 2.0.4 on 2018-08-10 05:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0014_auto_20180810_1142'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='level_index_field',
            field=models.CharField(default='', max_length=500, verbose_name='Индекс сложенности'),
        ),
    ]
