# Generated by Django 2.0.4 on 2018-08-08 03:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0010_auto_20180808_0918'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='good',
            name='manufacturer',
        ),
    ]
