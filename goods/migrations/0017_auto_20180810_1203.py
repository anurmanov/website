# Generated by Django 2.0.4 on 2018-08-10 06:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0016_auto_20180810_1159'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='level_index_field',
            field=models.CharField(default='', editable=False, max_length=500, verbose_name='Индекс вложенности'),
        ),
    ]
