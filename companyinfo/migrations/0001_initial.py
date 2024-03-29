# Generated by Django 2.0.4 on 2018-11-05 04:17

from django.db import migrations, models
import tinymce.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CompanyInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=50, verbose_name='код параметра')),
                ('name', models.CharField(max_length=50, verbose_name='название параметра')),
                ('value', tinymce.models.HTMLField(verbose_name='Value')),
            ],
            options={
                'verbose_name': 'информация о компании',
                'verbose_name_plural': 'информация о компании',
                'ordering': ['name'],
            },
        ),
    ]
