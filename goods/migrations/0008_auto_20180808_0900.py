# Generated by Django 2.0.4 on 2018-08-08 03:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0007_auto_20180808_0803'),
    ]

    operations = [
        migrations.AlterField(
            model_name='good',
            name='manufacturer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='goods.Manufacturer', verbose_name='Производитель'),
        ),
    ]