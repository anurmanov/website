# Generated by Django 2.0.4 on 2018-08-03 02:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0004_auto_20180801_1227'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='image',
            field=models.ImageField(default=None, null=True, upload_to='categories/images', verbose_name='Изображение'),
        ),
        migrations.AlterField(
            model_name='good',
            name='image',
            field=models.ImageField(default=None, null=True, upload_to='goods/images', verbose_name='Изображение'),
        ),
    ]
