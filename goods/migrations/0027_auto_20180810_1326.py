# Generated by Django 2.0.4 on 2018-08-10 07:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0026_auto_20180810_1322'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='level_index_field',
            field=models.CharField(default=None, max_length=500, null=True, verbose_name='Индекс вложенности'),
        ),
    ]