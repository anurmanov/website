# Generated by Django 2.0.4 on 2018-08-10 02:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0012_good_manufacturer'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ['name'], 'verbose_name': 'категория', 'verbose_name_plural': 'категории'},
        ),
        migrations.AlterModelOptions(
            name='country',
            options={'ordering': ['name'], 'verbose_name': 'страна', 'verbose_name_plural': 'страны'},
        ),
        migrations.AlterModelOptions(
            name='good',
            options={'ordering': ['name'], 'verbose_name': 'товар', 'verbose_name_plural': 'товары'},
        ),
        migrations.AlterModelOptions(
            name='manufacturer',
            options={'ordering': ['name'], 'verbose_name': 'производитель', 'verbose_name_plural': 'производители'},
        ),
    ]
